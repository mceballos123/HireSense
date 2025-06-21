# Backend - Fetch.ai uAgent Framework

This directory contains the backend setup for the Fetch.ai uAgent framework.

## Setup

1. **Virtual Environment**: A Python virtual environment is already set up in the `venv/` directory.

2. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies** (if needed):
   ```bash
   pip install -r requirements.txt
   ```

## Running the Agents

### Example Agent (with network connectivity handling)
```bash
source venv/bin/activate
python example_agent.py
```
- Runs on port 8000
- Handles network connectivity gracefully
- Includes wallet funding check (optional)

### Simple Agent (local only)
```bash
source venv/bin/activate
python simple_agent.py
```
- Runs on port 8001
- No network dependencies
- Perfect for local development and testing

## Project Structure

- `venv/` - Python virtual environment
- `requirements.txt` - Python dependencies
- `example_agent.py` - Full-featured uAgent example with network handling
- `simple_agent.py` - Basic uAgent example for local development
- `README.md` - This file

## uAgent Framework Features

The Fetch.ai uAgent framework provides:
- Autonomous agent creation and management
- Blockchain integration capabilities
- Message passing between agents
- Built-in wallet functionality
- Async/await support for concurrent operations
- Local development mode without network requirements

## Network Connectivity

- **Local Development**: Agents can run without network connectivity
- **Network Errors**: The framework gracefully handles network connectivity issues
- **Production**: For full blockchain integration, ensure network connectivity to Fetch.ai nodes

## Next Steps

1. Customize the example agents for your specific use case
2. Add more agents for different functionalities
3. Implement agent-to-agent communication
4. Integrate with blockchain networks as needed
5. Connect with your Next.js frontend application 