import logging
import re

from odoo import api, models, tools
from odoo.exceptions import MissingError, ValidationError


class InstallerHelper(models.AbstractModel):

    _name = 'installer.helper'
    _description = 'Helper to perform tasks when installing/upgrading a module'

    @api.model
    def run_only_once(self, installer, function_list):
        icp_env = self.env['ir.config_parameter']
        installer_env = self.env[installer]

        icp_key = 'installer_run_only_once_functions_done'
        functions_done = icp_env.get_param(icp_key)
        logging.info('run_only_once: functions already done: %s',
                     functions_done)
        functions_done = functions_done and functions_done.split('\n') or []

        for f in function_list:
            f_key = installer + ':' + f
            if f_key in functions_done:
                logging.info('skip run_only_once: %s (already done)' % f)
                continue
            logging.info('start run_only_once: %s', f)
            getattr(installer_env, f)()
            logging.info('end run_only_once: %s', f)
            functions_done.append(f_key)

        if functions_done:
            functions_done_str = '\n'.join(sorted(functions_done))
            icp_env.set_param(icp_key, functions_done_str)

        logging.info('All run_only_once functions of %s executed.', installer)

        return True

    @api.model
    def start(self):
        self.run_only_once(self._name, [
            'update_signup_setting',
        ])
        self.set_admin_full_accounting_features()
        return True

    @api.model
    def update_signup_setting(self):

        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('auth_signup.reset_password', True)
        set_param('auth_signup.invitation_scope', 'b2b')
        return True

    @api.model
    def install_modules(self, list_modules=False):
        if not list_modules:
            list_modules = {}

        ir_module_module = self.env["ir.module.module"]

        for mod_name in list_modules:
            mod = ir_module_module.search([('name', '=', mod_name)])
            if not mod:
                logging.warning(
                    'Module %s not found, updating list...',
                    mod_name)
                mod.update_list()
                mod = ir_module_module.search([('name', '=', mod_name)])
                if not mod:
                    raise MissingError("Module %s is not available." % mod_name)
            logging.info("Module %s is in status: %s", mod_name, mod.state)
            if mod.state == 'uninstalled':
                logging.info("Installing module %s", mod_name)
                mod.button_immediate_install()
            elif mod.state in ('installed', 'to upgrade'):
                logging.info("Module %s already installed.", mod_name)
                continue
            else:
                raise ValidationError(
                    ("The module %s is in an unexpected status: %s. "
                     "Check from the Apps menu.") % (
                        mod_name, mod.state))

    @api.model
    def install_lang(self, lang_codes=False):
        if not lang_codes:
            lang_codes = ['fr_FR']
        logging.info("start: install lang %s " % lang_codes)
        for lang_code in lang_codes:
            lang_installer_record = self.env['base.language.install'].create({
                'lang': lang_code, 'overwrite': True, })
            lang_installer_record.lang_install()
        logging.info("done: lang installed")
        return True

    @api.model
    def set_report_url(self):
        """
        Attempt to fix css missing issue mentionned here:
        https://www.odoo.com/documentation/10.0/howtos/backend.html#reporting
        """

        report_key_url = 'report.url'

        odoo_host = tools.config.get('http_interface')
        if not odoo_host:
            odoo_host = tools.config.get('xmlrpc_interface', '127.0.0.1')
        if odoo_host == '0.0.0.0':
            odoo_host = '127.0.0.1'

        odoo_port = tools.config.get('http_port')
        if not odoo_port:
            odoo_port = tools.config.get('xmlrpc_port', '8069')

        report_url = 'http://{}:{}/'.format(odoo_host, odoo_port)
        icp_env = self.env['ir.config_parameter']
        icp_env.set_param(report_key_url, report_url)

        return True

    @api.model
    def activate_currency(self, currencies):
        currencies = self.env['res.currency'].search(
            [('name', 'in', currencies), '|',
             ('active', '=', True),
             ('active', '=', False)])
        logging.info("activating currencies: %s",
                     ', '.join([c.name for c in currencies]))
        currencies.write({'active': True})

    @api.model
    def set_vnd_rounding_to_one(self):
        self.env.ref('base.VND').rounding = 1

    @api.model
    def set_allowed_companies_for_admin_user(self):
        self.env.ref('base.user_root').write({
            'company_ids': [
                (6, 0, self.env['res.company'].search([]).ids)
            ]
        })

    @api.model
    def set_admin_full_accounting_features(self):
        full_accounting = self.env.ref('account.group_account_user',
                                       raise_if_not_found=False)
        if not full_accounting:
            # account_user does not exist, probably because account module
            # is not installed.
            return
        # Check if using enterprise version, we just need to set this in
        # community version
        if full_accounting.name != 'Show Full Accounting Features':
            return
        admin_user = self.env.ref('base.user_root')
        if not admin_user.has_group('account.group_account_user'):
            admin_user.write({'groups_id': [(4, full_accounting.id)]})

    @api.model
    def save_role_functional_admin(self):
        """
        Shortcut to call save_role_functional_admin
        But you will probably need to specify a list of technical settings
        to add to the functional admin role for your project, then you should
        not use this shortcut.
        :return:
        """
        self.env['res.users.role'].save_role_functional_admin()
        return True

    @api.model
    def format_date_time(self, date_format='%d/%m/%Y', time_format='%H:%M:%S'):
        logging.info("start: install date format %s " % date_format)
        logging.info("start: install time format %s " % time_format)
        lang_model = self.env['res.lang'].search([])
        for rec in lang_model:
            rec.write({
                'date_format': date_format,
                'time_format': time_format,
            })
        logging.info("done: date and time format installed")
        return True

    @api.model
    def set_chart_of_account(self, company, coa_template_ref):
        coa_template = self.env.ref(coa_template_ref)
        self.env.user.company_id = company
        coa_template.load_for_current_company(10.0, 10.0)
        return True

    @api.model
    def set_ir_model_access_by_section(self, module, section_security_dict):
        """
        ## params
        section_security_dict: a dictionary with the following format:
        {
            "Billing Manager": {  # section security configuration
                "CRUD": [1, 1, 1, 0],
                "groups": ['account.group_account_advisor', ]
                "models": ['account.invoice', 'account.invoice.line],
            },
            "Billing Viewer": {  # section security configuration
                "CRUD": [0, 1, 0, 0],
                "groups": ['sales.group_sale_user', ]
                "models": ['account.invoice', 'account.invoice.line],
            },
            "Legal Accounting Manager": {  # section security configuration
                "CRUD": [1, 1, 1, 0],
                "groups": ['account.group_account_advisor', ]
                "models": ['account.move', 'account.move.line],
            },
            ....
        }

        # action
        For each section, for each groups, for each model,
        set the CRUD ir.model.access
        Search of existing ir.model.access for this model and group:
          - if exist, then update
          - if not exist, then create

        """
        logging.info("Start: Set up access by section")
        ir_model_access_env = self.env['ir.model.access']
        ir_model_env = self.env['ir.model']

        data_list = []

        for section, value in section_security_dict.items():
            for group in value.get('groups', []):
                res_group = self.env.ref(group, False)
                if not res_group:
                    raise MissingError(
                        "Can not find the group with xml_id '%s'"
                        "in systems!" % group)
                for model_name in value.get('models', []):
                    # Model field in ir.model table is unique.
                    model = \
                        ir_model_env.search([('model', '=', model_name), ])
                    if not model:
                        raise MissingError(
                            'Can not find the model %s in'
                            ' systems!' % model_name)
                    domain = [
                        ('group_id', '=', res_group.id),
                        ('model_id', '=', model.id),
                    ]
                    ir_model_access = \
                        ir_model_access_env.search(domain)

                    name = 'access_%s_%s_%s' % (
                        model_name.replace('.', '-'),
                        section.replace(' ', '-'),
                        group.split('.')[1]
                    )
                    if re.match("^[a-zA-Z0-9-_]*$", name) is None:
                        raise ValidationError(
                            "You must use a normalized name containing only "
                            "letters or - or _: %s" % name)

                    ir_model_access_vals = {
                        'name': name,
                        'perm_create': value['CRUD'][0],
                        'perm_read': value['CRUD'][1],
                        'perm_write': value['CRUD'][2],
                        'perm_unlink': value['CRUD'][3],
                    }
                    if ir_model_access:
                        if len(ir_model_access) > 1:
                            logging.warning(
                                "Found several ir.model.access for %s: %s",
                                domain,
                                ir_model_access.mapped('name')
                            )
                            ir_model_access = ir_model_access[0]
                        has_updates = (
                            (
                                ir_model_access.name
                                != name
                            )
                            or (
                                ir_model_access.perm_create
                                != ir_model_access_vals['perm_create']
                            )
                            or (
                                ir_model_access.perm_read
                                != ir_model_access_vals['perm_read']
                            )
                            or (
                                ir_model_access.perm_write
                                != ir_model_access_vals['perm_write']
                            )
                            or (
                                ir_model_access.perm_unlink
                                != ir_model_access_vals['perm_unlink']
                            )
                        )
                        if has_updates:
                            action = 'Update'
                            ir_model_access.write(ir_model_access_vals)
                        else:
                            action = 'Unchanged'
                    else:
                        action = 'Create'
                        ir_model_access_vals.update({
                            'model_id': model.id,
                            'group_id': res_group.id,
                        })
                        ir_model_access = ir_model_access_env.create(
                            ir_model_access_vals)

                    xml_id = '%s.%s' % (module, name)

                    data_list.append({
                        'xml_id': xml_id,
                        'record': ir_model_access,
                        'noupdate': False,

                    })

            msg = '%s ir.model.access for %s %s: %s' % (
                action,
                res_group.name,
                model_name,
                ir_model_access_vals
            )
            if action == 'Unchanged':
                logging.info(msg)
            else:
                logging.warning(msg)

        """ Create or update the given XML ids.
            :param data_list: list of dicts with keys `xml_id` (XMLID to
                assign), `noupdate` (flag on XMLID), `record` (target record).
            :param update: should be ``True`` when upgrading a module
        """
        self.env['ir.model.data']._update_xmlids(data_list, update=True)

        logging.info("Done: Set up access by section")
        return True
