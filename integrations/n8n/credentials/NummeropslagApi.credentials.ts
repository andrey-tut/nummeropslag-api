import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class NummeropslagApi implements ICredentialType {
	name = 'nummeropslagApi';

	displayName = 'Nummeropslag API';

	icon = 'file:../nodes/Nummeropslag/nummeropslag.svg' as const;

	documentationUrl =
		'https://github.com/andrey-tut/nummeropslag-api/tree/main/integrations/n8n#credentials';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			required: true,
			default: '',
			description: 'Get a key at https://nummeropslag.dk/api-noegle',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				'X-API-Key': '={{$credentials.apiKey}}',
				'X-Client': 'n8n',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://nummeropslag.dk/api/v1/partner',
			url: '/me',
		},
	};
}
