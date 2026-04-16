import asyncio
import os
import sys
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from smolagents import CodeAgent, InferenceClientModel, ToolCollection

# 1. Configuration initiale
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

server_params = StdioServerParameters(
    command=sys.executable,
    args=["weather_server.py"],
    env=None
)


# 2. Fonctions d'inspection (Ex 3.2 & 3.3)
async def inspect_server():
    print("--- INSPECTION DU SERVEUR ---")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"Outils disponibles : {[t.name for t in tools.tools]}")
            res = await session.list_resources()
            print(f"Ressources disponibles : {[r.name for r in res.resources]}")


# 3. Test de l'Agent Hugging Face (Ex 4.2)
def run_hf_agent():
    if not HF_TOKEN:
        print("Erreur : HF_TOKEN manquant dans le .env")
        return

    model_hf = InferenceClientModel(
        model_id="Qwen/Qwen2.5-72B-Instruct",
        token=HF_TOKEN
    )

    with ToolCollection.from_mcp(server_params, trust_remote_code=True) as mcp_tools:
        agent = CodeAgent(
            tools=[*mcp_tools.tools],
            model=model_hf,
            add_base_tools=True,
            verbosity_level=2
        )

        query = "Je prévois un voyage de Paris à Lyon. Vérifie les villes, la météo à Lyon, et le temps à 110 km/h."
        response = agent.run(query)
        print(f"\n🏁 RÉPONSE FINALE :\n{response}")


async def main():
    # Vous pouvez choisir quoi lancer ici
    await inspect_server()
    print("\n" + "=" * 30 + "\n")
    # Note: run_hf_agent est bloquant à cause du context manager de smolagents
    run_hf_agent()


if __name__ == "__main__":
    asyncio.run(main())