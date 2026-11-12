"""Pay one MCP tool call with x402 (USDC on Base).

Usage: python pay_mcp.py https://revalidation.amacunia.fr/mcp revalidation_lookup '{"npi": "1306897277"}'
  PAYER_PRIVATE_KEY  private key of the paying wallet (set by the caller, never printed);
  X402_NETWORK       eip155:8453 (Base) for real calls, eip155:84532 (Base Sepolia) for tests.
Dependencies: x402[evm,mcp], mcp, eth-account.
"""
import asyncio
import json
import os
import sys

from eth_account import Account
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from x402 import x402Client
from x402.mcp.client import x402MCPSession
from x402.mechanisms.evm.exact import ExactEvmClientScheme
from x402.mechanisms.evm.signers import EthAccountSigner


async def main(url: str, tool: str, arguments: dict) -> None:
    c = x402Client()
    c.register(os.environ.get("X402_NETWORK", "eip155:84532"),
               ExactEvmClientScheme(EthAccountSigner(Account.from_key(os.environ["PAYER_PRIVATE_KEY"]))))
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            s = x402MCPSession(session, c)
            await s.initialize()
            print("tools:", [t.name for t in (await s.list_tools()).tools])
            r = await s.call_tool(tool, arguments)
            print("paid:", r.payment_made, "| error:", r.is_error)
            print("settlement:", str(r.payment_response)[:300])
            print((r.content[0].text if r.content else "")[:400])


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2], json.loads(sys.argv[3])))
