#/usr/bin/env bash
_thus_completions_cc_functions()
{
case "${COMP_WORDS[COMP_CWORD-1]}" in 
	apikey)
		 COMPREPLY=($(compgen -W "describe list " "${COMP_WORDS[3]}"))
		 return
		;;
	accounts)
		 COMPREPLY=($(compgen -W "access botsetting create delete detail list rulesetting rulesettings scan subscription update updaterulesetting updaterulesettings " "${COMP_WORDS[3]}"))
		 return
		;;
	checks)
		 COMPREPLY=($(compgen -W "create delete describe list update " "${COMP_WORDS[3]}"))
		 return
		;;
	events)
		 COMPREPLY=($(compgen -W "list " "${COMP_WORDS[3]}"))
		 return
		;;
	externalid)
		 COMPREPLY=($(compgen -W "create get " "${COMP_WORDS[3]}"))
		 return
		;;
	profiles)
		 COMPREPLY=($(compgen -W "apply create delete describe list update " "${COMP_WORDS[3]}"))
		 return
		;;
	reportconfigs)
		 COMPREPLY=($(compgen -W "create delete describe list update " "${COMP_WORDS[3]}"))
		 return
		;;
	resources)
		 COMPREPLY=($(compgen -W "excludedresources " "${COMP_WORDS[3]}"))
		 return
		;;
	rules)
		 COMPREPLY=($(compgen -W "list " "${COMP_WORDS[3]}"))
		 return
		;;
	settings)
		 COMPREPLY=($(compgen -W "create list delete describe update " "${COMP_WORDS[3]}"))
		 return
		;;
	templatescanner)
		 COMPREPLY=($(compgen -W "scan " "${COMP_WORDS[3]}"))
		 return
		;;
	users)
		 COMPREPLY=($(compgen -W "addssouser currentuser describe invite list revoke update " "${COMP_WORDS[3]}"))
		 return
		;;
esac
}
_thus_completions_cc_classes()
{
COMPREPLY=($(compgen -W "apikey accounts checks events externalid profiles reportconfigs resources rules settings templatescanner users " "${COMP_WORDS[2]}"))
return
}
_thus_completions_ds_functions()
{
case "${COMP_WORDS[COMP_CWORD-1]}" in 
	apikeys)
		 COMPREPLY=($(compgen -W "current create currentsecretkey delete describe generatesecret list modify modifycurrent search " "${COMP_WORDS[3]}"))
		 return
		;;
	apiusagemetrics)
		 COMPREPLY=($(compgen -W "list search " "${COMP_WORDS[3]}"))
		 return
		;;
	administrators)
		 COMPREPLY=($(compgen -W "create createrole delete deleterole describe describerole list listroles modify modifyrole search searchrole " "${COMP_WORDS[3]}"))
		 return
		;;
	agentdeploymentscripts)
		 COMPREPLY=($(compgen -W "generate " "${COMP_WORDS[3]}"))
		 return
		;;
	antimalware)
		 COMPREPLY=($(compgen -W "create createdfileextensionlist createdfilelist createdirectorylist createdschedules delete deletedirectorylist deletefileextensionlist deletefilelist deleteschedule describe describedirectorylist describefileextensionlist describefilelist describeschedule list listdirectorylists listfileextensionlists listfilelists listschedules modify modifydirectorylist modifyfileextensionlist modifyfilelist modifyschedule search searchdirectorylist searchfileextensionlist searchfilelist searchschedule " "${COMP_WORDS[3]}"))
		 return
		;;
	applicationcontrol)
		 COMPREPLY=($(compgen -W "createglobalrule createsoftwareinventory createruleset deleteglobalrule deletesoftwareinventory deleteruleset deleterulesetrule describeglobalrule describerulesetrule describesoftwareinventory describesoftwareinventoryitem describesoftwarechange listglobalrules listsoftwareinventories listsoftwareinventoryitems listrulesetrules listrulesets listsoftwarechanges modifyglobalrule modifyruleset modifyrulesetrule reviewsoftwarechange searchglobalrules searchsoftwareinventory searchsoftwareinventoryitems searchrulesetrules searchrulesets searchsoftwarechanges " "${COMP_WORDS[3]}"))
		 return
		;;
	certificates)
		 COMPREPLY=($(compgen -W "add delete describe getbyurl list " "${COMP_WORDS[3]}"))
		 return
		;;
	computergroups)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	computers)
		 COMPREPLY=($(compgen -W "addfirewallassignment addintegritymonitoringassignments assignintrusionpreventionassignment assignloginspectionassignment create createintrusionpreventionassignment delete deletecomputerintrusionpreventionassignment deletefirewallassignment deleteintegritymonitoringassignments deleteintegritymonitoringrules deleteintrusionpreventionapplicationtypes deleteintrusionpreventionrules deleteloginspectionassignment deleteloginspectionrule describe describefirewallrules describeintegritymonitoringrules describeintrusionpreventionapplicationtypes describeintrusionpreventionrule describeloginspectionrule describesetting list listfirewallassignment listfirewallrules listintegritymonitoringassignments listintegritymonitoringrules listintrusionpreventionapplicationtypes listintrusionpreventionassignment listintrusionpreventionrules listloginspectionassignment listloginspectionrules modify modifyfirewallrules modifyintegritymonitoringrules modifyintrusionpreventionapplicationtypes modifyintrusionpreventionrule modifyloginspectionrule modifysetting resetfirewallrules resetsetting search setfirewallassignment setintegritymonitoringassignments setloginspectionassignment " "${COMP_WORDS[3]}"))
		 return
		;;
	contacts)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	eventbasedtasks)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	integritymonitoring)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	intrusionprevention)
		 COMPREPLY=($(compgen -W "createrules createtype deleterule deletetype describerule listrules listtypes modifyrule modifytype searchrules searchtypes " "${COMP_WORDS[3]}"))
		 return
		;;
	loginspectionrules)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	policies)
		 COMPREPLY=($(compgen -W "addfirewallruleassignments addintrusionpreventionruleassignments addloginspectionruleassignments setfirewallrulesassignments setintrusionpreventionrulesassignments setloginspectionrulesassignments addintegritymonitoringruleassignments create delete deletedefaultsetting deletefirewallruleassignments deleteintegritymonitoringrules deleteintrusionpreventionruleassignments deleteloginspectionruleassignments describe describedefaultsetting describefirewallrules describeintegritymonitoringrules describeintrusionpreventionapplication describeintrusionpreventionrules describeloginspection describepolicydefault list listfirewallrules listfirewallrulesassignments listintegritymonitoringrules listintegritymonitoringrulesassignments listintrusionpreventionapplication listintrusionpreventionrules listintrusionpreventionrulesassignments listloginspection listloginspectionrulesassignments listpolicydefault modify modifydefaultsetting modifyfirewallrules modifyintegritymonitoringrules modifyintrusionpreventionapplication modifyintrusionpreventionrules modifyloginspection modifypolicydefault modifypolicysetting removeintegritymonitoringruleassignments resetfirewallrules resetintrusionpreventionapplication resetintrusionpreventionrules resetloginspection resetpolicysetting search setintegritymonitoringruleassignments " "${COMP_WORDS[3]}"))
		 return
		;;
	reporttemplates)
		 COMPREPLY=($(compgen -W "describe list search " "${COMP_WORDS[3]}"))
		 return
		;;
	scheduledtasks)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	scripts)
		 COMPREPLY=($(compgen -W "list " "${COMP_WORDS[3]}"))
		 return
		;;
	systemsettings)
		 COMPREPLY=($(compgen -W "delete describe list modify " "${COMP_WORDS[3]}"))
		 return
		;;
	tenants)
		 COMPREPLY=($(compgen -W "create createapikey delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	firewall)
		 COMPREPLY=($(compgen -W "create createcontext createinterfacetype createstatefulconfiguration createiplists createmaclists createportlists delete deletecontext deleteiplist deleteinterfacetype deletestatefulconfiguration deletemaclist deleteportlist describe describecontext describeiplist describeinterfacetype describestatefulconfiguration describemaclist describeportlist list listcontexts listiplists listinterfacetypes listmaclists listportlists liststatefulconfigurations modify modifycontext modifyiplist modifyinterfacetype modifystatefulconfiguration modifymaclist modifyportlist search searchcontexts searchiplists searchinterfacetypes searchstatefulconfigurations searchmaclists searchportlists " "${COMP_WORDS[3]}"))
		 return
		;;
	gcpconnector)
		 COMPREPLY=($(compgen -W "create createaction delete describe describeaction list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
esac
}
_thus_completions_ds_classes()
{
COMPREPLY=($(compgen -W "apikeys apiusagemetrics administrators agentdeploymentscripts antimalware applicationcontrol certificates computergroups computers contacts eventbasedtasks integritymonitoring intrusionprevention loginspectionrules policies reporttemplates scheduledtasks scripts systemsettings tenants firewall gcpconnector " "${COMP_WORDS[2]}"))
return
}
_thus_completions_cs_functions()
{
case "${COMP_WORDS[COMP_CWORD-1]}" in 
	contentrules)
		 COMPREPLY=($(compgen -W "createcontentruleset createcontentrulesetcollection deletecontentruleset deletecontentrulesetcollection describecontentruleset describecontentrulesetcollection listcontentruleset listcontentrulesetcollections modifycontentruleset modifycontentrulesetcollection " "${COMP_WORDS[3]}"))
		 return
		;;
	identityproviders)
		 COMPREPLY=($(compgen -W "createsaml deletesaml describesaml listsaml modifysaml " "${COMP_WORDS[3]}"))
		 return
		;;
	license)
		 COMPREPLY=($(compgen -W "describe " "${COMP_WORDS[3]}"))
		 return
		;;
	overrides)
		 COMPREPLY=($(compgen -W "createchecklistfindingoverride createcontentfindingoverride createvulnerabilityfindingoverride deletechecklistfindingoverride deletecontentfindingoverride deletevulnerabilityfindingoverride describechecklistfindingoverride describecontentfindingoverride describevulnerabilityfindingoverride listchecklistfindingoverrides listcontentfindingoverrides listvulnerabilityfindingoverrides modifychecklistfindingoverride modifycontentfindingoverride modifyvulnerabilityfindingoverride " "${COMP_WORDS[3]}"))
		 return
		;;
	registries)
		 COMPREPLY=($(compgen -W "create createregistryscan delete describe describeregistrydashboard describeregistryimage list listregistryimages modify " "${COMP_WORDS[3]}"))
		 return
		;;
	roles)
		 COMPREPLY=($(compgen -W "create deletesession describe list modify " "${COMP_WORDS[3]}"))
		 return
		;;
	scans)
		 COMPREPLY=($(compgen -W "cancel create describe describeconfigurationchecklist describescanmetrics list listconfigurationchecklistprofilerules listlayercontentfindingsscans listlayermalwarefindingsscans listlayervulnerabilityfindingsscans listscanchecklist " "${COMP_WORDS[3]}"))
		 return
		;;
	sessions)
		 COMPREPLY=($(compgen -W "create delete describe list refresh " "${COMP_WORDS[3]}"))
		 return
		;;
	users)
		 COMPREPLY=($(compgen -W "changepassword create delete describe list modify " "${COMP_WORDS[3]}"))
		 return
		;;
	webhook)
		 COMPREPLY=($(compgen -W "create delete describe list modify " "${COMP_WORDS[3]}"))
		 return
		;;
esac
}
_thus_completions_cs_classes()
{
COMPREPLY=($(compgen -W "contentrules identityproviders license overrides registries roles scans sessions users webhook " "${COMP_WORDS[2]}"))
return
}
_thus_completions()
{
  local cloudone_services="deepsecurity ds smartcheck sc workloadsecurity ws containersecurity cs cc cloudconformity" 
  COMPREPLY=()
  if [ "${#COMP_WORDS[@]}" == "2" ]; then
    COMPREPLY=($(compgen -W "${cloudone_services}" "${COMP_WORDS[1]}")) 
    return
  fi
  service=${COMP_WORDS[1]}
  case ${service} in 
    workloadsecurity | ws | ds) 
        service="deepsecurity" 
       ;; 
    containersecurity | cs | sc) 
        service="smartcheck" 
        ;;
    cloudconformity | cc) 
        service="cloudconformity" 
        ;;
    esac
  if [ "${#COMP_WORDS[@]}" == "3" ]; then
    case ${service} in
         deepsecurity)
              _thus_completions_ds_classes
              return
         ;;
         smartcheck)
             _thus_completions_cs_classes
             return
         ;;
         cloudconformity)
             _thus_completions_cc_classes
             return
         ;;
     esac
     return
   fi
    if [ "${#COMP_WORDS[@]}" == "4" ]; then
    case ${service} in
        deepsecurity)
            _thus_completions_ds_functions
            return
        ;;
        smartcheck)
            _thus_completions_cs_functions
            return
        ;;
        cloudconformity)
            _thus_completions_cc_functions
            return
        ;;
    esac
    return
  fi
}
complete -F _thus_completions thus
