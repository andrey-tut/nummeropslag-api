# Nummeropslag for Dify

Nummeropslag adds privacy-first Danish caller ID and business lookup tools to
Dify Chatflows, Workflows and Agents.

## Tools

- Look up a Danish phone number.
- Check a number for spam or scam signals.
- Get the operator and number type.
- Search Danish businesses by name.
- Inspect API scopes and remaining quota.

The results combine official CVR and Danish number-plan data with anonymous
community spam reports. The service never requires contact uploads and does not
return names of private individuals.

## Setup

1. Get an API key at <https://nummeropslag.dk/api-noegle>.
2. Install the packaged Nummeropslag plugin in Dify.
3. Add a Nummeropslag provider credential and paste the API key.
4. Add any of the tools to a Workflow, Chatflow or Agent.

Example Agent request: `Is +45 70 10 20 30 likely to be spam?`

API documentation: <https://andrey-tut.github.io/nummeropslag-api/>

Source: <https://github.com/andrey-tut/nummeropslag-api>

Contact: <info@lynbro.dk>
