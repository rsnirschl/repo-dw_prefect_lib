from prefect import variables

env_vars = {
		"vEnv_Analytics_DB": {
		"dev": "DEV_ANALYTICS",
		"prd": "PRD_ANALYTICS",
		"tst": "TST_ANALYTICS"
	},
		"vEnv_Dbt_Job_ID": {
		"dev": "102222",
		"prd": "102504",
		"tst": "122561"
	},
		"vEnv_Heritage_Daily_File_Path": {
		"dev": "smb://tstftp01.mutualofenumclaw.net/ev1/MACS/archive/",
		"prd": "smb://prdftp01.mutualofenumclaw.net/PRD/MACS/archive/",
		"tst": "smb://tstftp01.mutualofenumclaw.net/ev1/MACS/archive/"
	},
		"vEnv_Heritage_Daily_S3_Bucket": {
		"dev": "dw-datalake-tst-us-west-2/heritage_daily_commissions/",
		"prd": "dw-datalake-prd-us-west-2/heritage_daily_commissions/",
		"tst": "dw-datalake-tst-us-west-2/heritage_daily_commissions/"
	},
		"vEnv_Heritage_File_Pwd": {
		"dev": "TSTFTP01",
		"prd": "PRDFTP01",
		"tst": "TSTFTP01"
	},
		"vEnv_Heritage_File_Username": {            
		"dev": "s_MatillionDevTstSha",
		"prd": "s_MatillionAccPrdSha",
		"tst": "s_MatillionDevTstSha"
	},
		"vEnv_SNS_Teams_Channel": {
		"dev": "https://enumclawpandc.webhook.office.com/webhookb2/5ef1a520-7b2f-4ffe-8ea9-26ec22498e61@5a381f7d-cc3d-4a93-b2cb-d2fd072e535a/IncomingWebhook/f6dbc645442a494791378b081d745d58/33dc186e-20d6-4b0f-b6c5-d8e5953d8571",
		"prd": "https://enumclawpandc.webhook.office.com/webhookb2/5ef1a520-7b2f-4ffe-8ea9-26ec22498e61@5a381f7d-cc3d-4a93-b2cb-d2fd072e535a/IncomingWebhook/76179be2cd2c409db7146bcd4f35f9d6/33dc186e-20d6-4b0f-b6c5-d8e5953d8571",
		"tst": "https://enumclawpandc.webhook.office.com/webhookb2/5ef1a520-7b2f-4ffe-8ea9-26ec22498e61@5a381f7d-cc3d-4a93-b2cb-d2fd072e535a/IncomingWebhook/4e5ba6eb928149fc807dfab14bd1b709/33dc186e-20d6-4b0f-b6c5-d8e5953d8571"
	},
		"vEnv_Storage_Integration": {
		"dev": "AWS_S3_TST",
		"prd": "AWS_S3_PRD",
		"tst": "AWS_S3_TST"
	},
        "vEnv_DBT_Credential_Block": {
		"dev": "dbt-cloud-creds",
		"prd": "dbt-cloud-creds",
		"tst": "dbt-cloud-creds"
    }
}

#env = 'dev'      #set by command parameter or maybe path parsing
env = variables.get('env')
for v in env_vars:
	exec(v + " = env_vars[v][env]")  # create the vars with the applicable env selected            