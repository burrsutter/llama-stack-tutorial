import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from "zod";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

const server = new Server(
  {
    name: "my-node-mcp-server-other",
    version: "1.0.0"
  },
  {
    capabilities: {
      tools: {},
    },
  },
);


// handler that returns list of available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'fetch_customer_details',
        description:
          'Find and return the customer details for the provided customer id',
        inputSchema: {
          type: 'object',
          properties: {
            customer_id: {
              type: 'string',
              description: 'customer id',
            }
          },
          required: ['customer_id'],
        },
      },
    ],
  };
});

// handler that invokes appropriate tool when called
server.setRequestHandler(CallToolRequestSchema, async request => {
  if (
    request.params.name === 'fetch_customer_details' 
  ) {

    const customer_id = request.params.arguments?.customer_id;
    
    
    let text = "looking for customer details based on customer id";

    if (customer_id) {
      if (request.params.name === 'fetch_customer_details') {          
        text = 
        "Customer " + customer_id + " is Jose McDonald with a balance of $100"
      } else {
        text = 
        "I need a customer id to return the customer details";
      }
    } 

    return {
      content: [
        {
          type: 'text',
          text: text,
        },
      ],
    };
  } else {
    throw new Error('Unknown tool');
  }
});



async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(error => {
  console.error('Server error:', error);
  process.exit(1);
});
