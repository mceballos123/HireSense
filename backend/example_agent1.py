from uagents import Agent, Context

# Create a simple agent without network dependencies
agent = Agent(
    name="simple_agent",
    port=8001,
    seed="simple_seed_phrase_here",
    endpoint=["http://127.0.0.1:8001/submit"],
)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Agent {agent.name} started successfully!")
    ctx.logger.info(f"Agent address: {agent.address}")

@agent.on_interval(period=5.0)
async def interval_handler(ctx: Context):
    ctx.logger.info(f"Agent {agent.name} is running... (interval check)")

if __name__ == "__main__":
    print("Starting simple uAgent...")
    print("This agent runs locally without network connectivity requirements.")
    agent.run() 