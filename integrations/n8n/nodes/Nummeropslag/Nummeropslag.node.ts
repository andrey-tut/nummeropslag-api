import { NodeConnectionTypes, type INodeType, type INodeTypeDescription } from 'n8n-workflow';

const phoneNumberField = {
	displayName: 'Danish Phone Number',
	name: 'number',
	type: 'string' as const,
	required: true,
	default: '',
	placeholder: '+45 33 63 33 63',
	description: 'An 8-digit Danish number or a number with the +45 country code',
};

export class Nummeropslag implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Nummeropslag',
		name: 'nummeropslag',
		icon: { light: 'file:nummeropslag.svg', dark: 'file:nummeropslag.dark.svg' },
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"]}}',
		description: 'Look up Danish callers, companies, operators and spam signals',
		defaults: {
			name: 'Nummeropslag',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [{ name: 'nummeropslagApi', required: true }],
		requestDefaults: {
			baseURL: 'https://nummeropslag.dk/api/v1/partner',
			headers: {
				Accept: 'application/json',
			},
		},
		properties: [
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Check Spam',
						value: 'spam',
						action: 'Check a danish number for spam',
						description: 'Get a compact spam and trust verdict',
						routing: {
							request: {
								method: 'GET',
								url: '={{"/spam/" + encodeURIComponent($parameter.number)}}',
							},
						},
					},
					{
						name: 'Get API Status',
						value: 'status',
						action: 'Get API key status',
						description: 'Get plan, scopes, quota and current usage',
						routing: {
							request: {
								method: 'GET',
								url: '/me',
							},
						},
					},
					{
						name: 'Get Operator',
						value: 'operator',
						action: 'Get the operator of a danish number',
						description: 'Get telecom operator and number type',
						routing: {
							request: {
								method: 'GET',
								url: '={{"/operator/" + encodeURIComponent($parameter.number)}}',
							},
						},
					},
					{
						name: 'Look Up Number',
						value: 'lookup',
						action: 'Look up a danish phone number',
						description: 'Get company, operator, spam/trust and recent comment data',
						routing: {
							request: {
								method: 'GET',
								url: '={{"/lookup/" + encodeURIComponent($parameter.number)}}',
							},
						},
					},
					{
						name: 'Search Businesses',
						value: 'search',
						action: 'Search danish businesses',
						description: 'Search the official CVR company register by business name',
						routing: {
							request: {
								method: 'GET',
								url: '/search',
							},
						},
					},
				],
				default: 'lookup',
			},
			{
				...phoneNumberField,
				displayOptions: {
					show: {
						operation: ['lookup', 'spam', 'operator'],
					},
				},
			},
			{
				displayName: 'Business Name',
				name: 'query',
				type: 'string',
				required: true,
				default: '',
				placeholder: 'LynBro',
				description: 'At least two characters from a Danish company name',
				displayOptions: {
					show: {
						operation: ['search'],
					},
				},
				routing: {
					send: {
						type: 'query',
						property: 'q',
					},
				},
			},
			{
				displayName: 'Limit',
				name: 'limit',
				type: 'number',
				default: 50,
				typeOptions: {
					minValue: 1,
					maxValue: 50,
				},
				description: 'Max number of results to return',
				displayOptions: {
					show: {
						operation: ['search'],
					},
				},
				routing: {
					send: {
						type: 'query',
						property: 'limit',
					},
				},
			},
		],
	};
}
