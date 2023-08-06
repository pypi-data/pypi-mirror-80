#compdef _thus thus
function _thus(){
    local line
    _arguments -C \
        "1: :(deepsecurity ds smartcheck sc workloadsecurity ws containersecurity cs)" \
        "*::arg:->args"
    case $line[1] in
        smartcheck | sc | cs | containersecurity)
            if [[ -z $line[2] ]]; then
              _thus_smartcheck_classes
            else
              _thus_completions_smartcheck_functions
            fi
        ;;
        deepsecurity | ds | ws | workloadsecurity)
         if [[ -z $line[2] ]]; then
            _thus_deepsecurity_classes
          else
              _thus_completions_deepsecurity_functions
            fi
        ;;
        cloudconformity | cc )
            if [[ -z $line[2] ]]; then
              _thus_cc_classes
            else
              _thus_completions_cc_functions
            fi
        ;;
    esac
}
function _thus_deepsecurity_classes() {
_arguments  "1: :( apikeys apiusagemetrics administrators agentdeploymentscripts antimalware applicationcontrol certificates computergroups computers contacts eventbasedtasks integritymonitoring intrusionprevention loginspectionrules policies reporttemplates scheduledtasks scripts systemsettings tenants firewall gcpconnector )"
return
}
function _thus_completions_deepsecurity_functions() {
  case $line[2] in
  apikeys )
    _arguments "2: :( current create currentsecretkey delete describe generatesecret list modify modifycurrent search )"
    return
    ;;
  apiusagemetrics )
    _arguments "2: :( list search )"
    return
    ;;
  administrators )
    _arguments "2: :( create createrole delete deleterole describe describerole list listroles modify modifyrole search searchrole )"
    return
    ;;
  agentdeploymentscripts )
    _arguments "2: :( generate )"
    return
    ;;
  antimalware )
    _arguments "2: :( create createdfileextensionlist createdfilelist createdirectorylist createdschedules delete deletedirectorylist deletefileextensionlist deletefilelist deleteschedule describe describedirectorylist describefileextensionlist describefilelist describeschedule list listdirectorylists listfileextensionlists listfilelists listschedules modify modifydirectorylist modifyfileextensionlist modifyfilelist modifyschedule search searchdirectorylist searchfileextensionlist searchfilelist searchschedule )"
    return
    ;;
  applicationcontrol )
    _arguments "2: :( createglobalrule createsoftwareinventory createruleset deleteglobalrule deletesoftwareinventory deleteruleset deleterulesetrule describeglobalrule describerulesetrule describesoftwareinventory describesoftwareinventoryitem describesoftwarechange listglobalrules listsoftwareinventories listsoftwareinventoryitems listrulesetrules listrulesets listsoftwarechanges modifyglobalrule modifyruleset modifyrulesetrule reviewsoftwarechange searchglobalrules searchsoftwareinventory searchsoftwareinventoryitems searchrulesetrules searchrulesets searchsoftwarechanges )"
    return
    ;;
  certificates )
    _arguments "2: :( add delete describe getbyurl list )"
    return
    ;;
  computergroups )
    _arguments "2: :( create delete describe list modify search )"
    return
    ;;
  computers )
    _arguments "2: :( addfirewallassignment addintegritymonitoringassignments assignintrusionpreventionassignment assignloginspectionassignment create createintrusionpreventionassignment delete deletecomputerintrusionpreventionassignment deletefirewallassignment deleteintegritymonitoringassignments deleteintegritymonitoringrules deleteintrusionpreventionapplicationtypes deleteintrusionpreventionrules deleteloginspectionassignment deleteloginspectionrule describe describefirewallrules describeintegritymonitoringrules describeintrusionpreventionapplicationtypes describeintrusionpreventionrule describeloginspectionrule describesetting list listfirewallassignment listfirewallrules listintegritymonitoringassignments listintegritymonitoringrules listintrusionpreventionapplicationtypes listintrusionpreventionassignment listintrusionpreventionrules listloginspectionassignment listloginspectionrules modify modifyfirewallrules modifyintegritymonitoringrules modifyintrusionpreventionapplicationtypes modifyintrusionpreventionrule modifyloginspectionrule modifysetting resetfirewallrules resetsetting search setfirewallassignment setintegritymonitoringassignments setloginspectionassignment )"
    return
    ;;
  contacts )
    _arguments "2: :( create delete describe list modify search )"
    return
    ;;
  eventbasedtasks )
    _arguments "2: :( create delete describe list modify search )"
    return
    ;;
  integritymonitoring )
    _arguments "2: :( create delete describe list modify search )"
    return
    ;;
  intrusionprevention )
    _arguments "2: :( createrules createtype deleterule deletetype describerule listrules listtypes modifyrule modifytype searchrules searchtypes )"
    return
    ;;
  loginspectionrules )
    _arguments "2: :( create delete describe list modify search )"
    return
    ;;
  policies )
    _arguments "2: :( addfirewallruleassignments addintrusionpreventionruleassignments addloginspectionruleassignments setfirewallrulesassignments setintrusionpreventionrulesassignments setloginspectionrulesassignments addintegritymonitoringruleassignments create delete deletedefaultsetting deletefirewallruleassignments deleteintegritymonitoringrules deleteintrusionpreventionruleassignments deleteloginspectionruleassignments describe describedefaultsetting describefirewallrules describeintegritymonitoringrules describeintrusionpreventionapplication describeintrusionpreventionrules describeloginspection describepolicydefault list listfirewallrules listfirewallrulesassignments listintegritymonitoringrules listintegritymonitoringrulesassignments listintrusionpreventionapplication listintrusionpreventionrules listintrusionpreventionrulesassignments listloginspection listloginspectionrulesassignments listpolicydefault modify modifydefaultsetting modifyfirewallrules modifyintegritymonitoringrules modifyintrusionpreventionapplication modifyintrusionpreventionrules modifyloginspection modifypolicydefault modifypolicysetting removeintegritymonitoringruleassignments resetfirewallrules resetintrusionpreventionapplication resetintrusionpreventionrules resetloginspection resetpolicysetting search setintegritymonitoringruleassignments )"
    return
    ;;
  reporttemplates )
    _arguments "2: :( describe list search )"
    return
    ;;
  scheduledtasks )
    _arguments "2: :( create delete describe list modify search )"
    return
    ;;
  scripts )
    _arguments "2: :( list )"
    return
    ;;
  systemsettings )
    _arguments "2: :( delete describe list modify )"
    return
    ;;
  tenants )
    _arguments "2: :( create createapikey delete describe list modify search )"
    return
    ;;
  firewall )
    _arguments "2: :( create createcontext createinterfacetype createstatefulconfiguration createiplists createmaclists createportlists delete deletecontext deleteiplist deleteinterfacetype deletestatefulconfiguration deletemaclist deleteportlist describe describecontext describeiplist describeinterfacetype describestatefulconfiguration describemaclist describeportlist list listcontexts listiplists listinterfacetypes listmaclists listportlists liststatefulconfigurations modify modifycontext modifyiplist modifyinterfacetype modifystatefulconfiguration modifymaclist modifyportlist search searchcontexts searchiplists searchinterfacetypes searchstatefulconfigurations searchmaclists searchportlists )"
    return
    ;;
  gcpconnector )
    _arguments "2: :( create createaction delete describe describeaction list modify search )"
    return
    ;;
 *)
    _thus_deepsecurity_classes
    ;;
  esac
}
function _thus_completions_smartcheck_functions() {
  case $line[2] in
  contentrules )
    _arguments "2: :( createcontentruleset createcontentrulesetcollection deletecontentruleset deletecontentrulesetcollection describecontentruleset describecontentrulesetcollection listcontentruleset listcontentrulesetcollections modifycontentruleset modifycontentrulesetcollection )"
    return
    ;;
  identityproviders )
    _arguments "2: :( createsaml deletesaml describesaml listsaml modifysaml )"
    return
    ;;
  license )
    _arguments "2: :( describe )"
    return
    ;;
  overrides )
    _arguments "2: :( createchecklistfindingoverride createcontentfindingoverride createvulnerabilityfindingoverride deletechecklistfindingoverride deletecontentfindingoverride deletevulnerabilityfindingoverride describechecklistfindingoverride describecontentfindingoverride describevulnerabilityfindingoverride listchecklistfindingoverrides listcontentfindingoverrides listvulnerabilityfindingoverrides modifychecklistfindingoverride modifycontentfindingoverride modifyvulnerabilityfindingoverride )"
    return
    ;;
  registries )
    _arguments "2: :( create createregistryscan delete describe describeregistrydashboard describeregistryimage list listregistryimages modify )"
    return
    ;;
  roles )
    _arguments "2: :( create deletesession describe list modify )"
    return
    ;;
  scans )
    _arguments "2: :( cancel create describe describeconfigurationchecklist describescanmetrics list listconfigurationchecklistprofilerules listlayercontentfindingsscans listlayermalwarefindingsscans listlayervulnerabilityfindingsscans listscanchecklist )"
    return
    ;;
  sessions )
    _arguments "2: :( create delete describe list refresh )"
    return
    ;;
  users )
    _arguments "2: :( changepassword create delete describe list modify )"
    return
    ;;
  webhook )
    _arguments "2: :( create delete describe list modify )"
    return
    ;;
 *)
    _thus_smartcheck_classes
    ;;
  esac
}
function _thus_smartcheck_classes() {
    _arguments "1: :(contentrules identityproviders license overrides registries roles scans sessions users webhook )"
    return
}
function _thus_cc_classes() {
    _arguments "1: :(apikey accounts checks events externalid profiles reportconfigs resources rules settings templatescanner users )"
    return
}
function _thus_completions_cc_functions() {
  case $line[2] in
  apikey )
    _arguments "2: :( describe list )"
    return
    ;;
  accounts )
    _arguments "2: :( access botsetting create delete detail list rulesetting rulesettings scan subscription update updaterulesetting updaterulesettings )"
    return
    ;;
  checks )
    _arguments "2: :( create delete describe list update )"
    return
    ;;
  events )
    _arguments "2: :( list )"
    return
    ;;
  externalid )
    _arguments "2: :( create get )"
    return
    ;;
  profiles )
    _arguments "2: :( apply create delete describe list update )"
    return
    ;;
  reportconfigs )
    _arguments "2: :( create delete describe list update )"
    return
    ;;
  resources )
    _arguments "2: :( excludedresources )"
    return
    ;;
  rules )
    _arguments "2: :( list )"
    return
    ;;
  settings )
    _arguments "2: :( create list delete describe update )"
    return
    ;;
  templatescanner )
    _arguments "2: :( scan )"
    return
    ;;
  users )
    _arguments "2: :( addssouser currentuser describe invite list revoke update )"
    return
    ;;
 *)
    _thus_cc_classes
    ;;
  esac
}
