from src.ruleScanner import RuleScanner

ruleScanner = RuleScanner()

pattern = "create or replace package body (@package_name <ident>) (is|as)"
pattern = ".blk"
#pattern = "type (<type_name> .id) is (<type_record>|<type_table>) ';'"
#pattern = "cursor (<cursor_name> .id) '(' !')'* ')' is"
#pattern = "(<variable_name> .id) (<variable_type> !';'.id) ';'"

list_rules = ruleScanner.str_split_syntax_rule(pattern)

print ('alternatives_found:',len(list_rules))
for i in range(0,len(list_rules)):
    print ('Elements found in alternative ',i,':')
    for el in list_rules[i]:
        print (el)

pattern = "!a"
list_rules = ruleScanner.str_split_token_rule(pattern)
print ("split token: ",list_rules)

pattern = "<test_rule>+"
list_rules = ruleScanner.str_split_rule_name(pattern)
print ("split rule: ",list_rules)
