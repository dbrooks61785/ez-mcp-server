import express from "express";
import dotenv from "dotenv";
import { Server } from "@modelcontextprotocol/sdk";

dotenv.config();

const app = express();
const port = 3030;

// Create MCP server
const mcpServer = new Server({
  name: "EZ Automation MCP",
  version: "1.0.0"
});

// Add a ping tool
mcpServer.addTool({
  name: "ping",
  description: "Return pong",
  execute: async () => {
    return { message: "pong" };
  }
});

// Attach HTTP handler
app.use(express.json());
app.post("/mcp", (req, res) => mcpServer.handleHTTPRequest(req, res));

// Start server
app.listen(port, () => {
  console.log(`MCP server running at http://localhost:${port}`);
});