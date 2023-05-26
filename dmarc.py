class DMARCExtractor:
    def __init__(self) -> None:
        self.base_data_relations_tree = {
            "version": "./version",
            "reporter_name": "./report_metadata/org_name",
            "reporter_mail": "./report_metadata/email",
            "report_id": "./report_metadata/report_id",
            "contact_info": "./report_metadata/extra_contact_info",
            "date_range_begin": "./report_metadata/date_range/begin",
            "date_range_end": "./report_metadata/date_range/end",
            "published_domian": "./policy_published/domain",
            "published_adkim": "./policy_published/adkim",
            "published_aspf": "./policy_published/aspf",
            "published_p": "./policy_published/p",
            "published_sp": "./policy_published/sp",
            "published_pct": "./policy_published/pct",
            "published_fo": "./policy_published/fo",
        }
        self.record_data_relations_tree = {
            "source_ip": "./row/source_ip",
            "count": "./row/count",
            "disposition": "./row/policy_evaluated/disposition",
            "dkim_action": "./row/policy_evaluated/dkim",
            "spf_action": "./row/policy_evaluated/spf",
            "header_from": "./identifiers/header_from",
            "envelope_from": "./identifiers/envelope_from",
            "envelope_to": "./identifiers/envelope_to",
            "dkim_domain": "./auth_results/dkim/domain",
            "dkim_result": "./auth_results/dkim/result",
            "dkim_selector": "./auth_results/dkim/selector",
            "spf_domain": "./auth_results/spf/domain",
            "spf_result": "./auth_results/spf/result",
            "spf_scope": "./auth_results/spf/scope",
        }

    def get_xml_value(self, xml, key):
        value = xml.find(key)
        return value.text if value is not None else "none"

    def extract_variables(self, xml):
        msg = ""

        reporter_org = self.get_xml_value(xml, "./report_metadata/org_name")
        print(f"A report from: {reporter_org} was logged")

        for name, key in self.base_data_relations_tree.items():
            msg += f"{name}={self.get_xml_value(xml, key)} "

        for record in xml.findall("./record"):
            for name, key in self.record_data_relations_tree.items():
                msg += f"{name}={self.get_xml_value(record, key)} "

        return msg
