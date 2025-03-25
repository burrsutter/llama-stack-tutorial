import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from "zod";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

const server = new Server(
  {
    name: "my-node-mcp-server-stdio",
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
        name: 'add',
        description:
          'adds to integers',
        inputSchema: {
          type: 'object',
          properties: {
            a: {
              type: 'int',
              description: 'the first integer',
            },
            b: {
              type: 'int',
              description: 'the second integer',
            },
          },
          required: ['a', 'b'],
        },
      },
      {
        name: 'subtract',
        description:
          'subtracts one integer from another',
        inputSchema: {
          type: 'object',
          properties: {
            a: {
              type: 'int',
              description: 'the first integer is the minuend',
            },
            b: {
              type: 'int',
              description: 'the second integer is subtrahend',
            },
          },
          required: ['a', 'b'],
        },
      },
    ],
  };
});

// handler that invokes appropriate tool when called
server.setRequestHandler(CallToolRequestSchema, async request => {
  if (
    request.params.name === 'add' ||
    request.params.name === 'subtract'
  ) {

    const a = request.params.arguments?.a;
    const b = request.params.arguments?.b;
    
    // This text gets overwritten if add or subtract are called
    let text = "add or subtract, give me two numbers";

    if (a && b) {
      if (request.params.name === 'add') {
          let c = a + b;
          text =
            a + '+' + b + ' = ' + c;
      } else if (request.params.name === 'subtract') {
          let c = a - b;
          text =
            'The subtraction answer is ' + c;
      }
    } // if (a && b)

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
