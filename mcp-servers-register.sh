# If using docker/podman to run Llama Stack Server
curl -X POST -H "Content-Type: application/json" --data '{ "provider_id" : "model-context-protocol", "toolgroup_id" : "mcp::my-node-server", "mcp_endpoint" : { "uri" : "http://host.docker.internal:3001/sse"}}' http://localhost:8321/v1/toolgroups
curl -X POST -H "Content-Type: application/json" --data '{ "provider_id" : "model-context-protocol", "toolgroup_id" : "mcp::my-python-server", "mcp_endpoint" : { "uri" : "http://host.docker.internal:8000/sse"}}' http://localhost:8321/v1/toolgroups

