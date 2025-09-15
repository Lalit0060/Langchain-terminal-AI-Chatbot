import getpass
import os
import time
import re
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import SystemMessage, HumanMessage

# Rich imports for markdown rendering
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text

def setup_environment():
    """Setup Google API key"""
    if not os.environ.get("GOOGLE_API_KEY"):
        print("🔑 Google API Key Setup Required")
        print("Get your API key from: https://aistudio.google.com/")
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google Gemini API key: ")
    
    try:
        from langchain.chat_models import init_chat_model
        return init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    except Exception as e:
        print(f"❌ Error initializing model: {e}")
        return None

def create_chatbot_app():
    """Create the LangGraph chatbot application"""
    model = setup_environment()
    if not model:
        return None
    
    workflow = StateGraph(state_schema=MessagesState)

    def call_model(state: MessagesState):
        system_prompt = """You are a helpful AI assistant that can provide responses in markdown format.
        Feel free to use markdown formatting like:
        - **bold text** and *italic text*
        - `code snippets`
        - Lists and bullet points
        - Headers with # ## ###
        - > Blockquotes
        - Code blocks with ```
        
        Make your responses visually appealing and well-structured."""
        
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = model.invoke(messages)
        return {"messages": response}

    workflow.add_node("model", call_model)
    workflow.add_edge(START, "model")

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

def is_likely_markdown(text):
    """Check if text contains markdown elements"""
    markdown_patterns = [
        r'\*\*.*?\*\*',  # Bold
        r'\*.*?\*',      # Italic
        r'`.*?`',        # Code
        r'^#+ ',         # Headers
        r'^\* ',         # Lists
        r'^\d+\. ',      # Numbered lists
        r'^> ',          # Blockquotes
        r'```',          # Code blocks
    ]
    return any(re.search(pattern, text, re.MULTILINE) for pattern in markdown_patterns)

def markdown_streaming_chat():
    """Rich markdown streaming chatbot"""
    console = Console()
    
    # Display header with Rich styling
    console.print("\n🤖 [bold cyan]LangChain Rich Markdown Streaming Chatbot[/bold cyan]")
    console.print("=" * 60)
    console.print("✨ [green]Features:[/green] Markdown rendering, Smooth streaming, Memory")
    console.print("💡 [yellow]Tip:[/yellow] Ask for formatted responses with lists, code, etc.")
    console.print("🚪 [red]Commands:[/red] 'quit', 'exit', 'bye' to end chat")
    console.print("=" * 60)
    
    app = create_chatbot_app()
    if not app:
        console.print("❌ [red]Failed to initialize chatbot. Exiting...[/red]")
        return
    
    thread_id = "markdown_session_1"
    
    while True:
        try:
            user_input = console.input("\n[bold blue]👤 You:[/bold blue] ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                console.print("\n🤖 [green]Thank you for chatting! Goodbye![/green] 👋")
                break
            
            # Start bot response
            console.print("🤖 [bold green]Bot:[/bold green] ", end="")
            
            # Collect response for markdown rendering
            response_buffer = ""
            display_buffer = ""
            
            try:
                # Create Live display for real-time markdown rendering
                with Live(console=console, refresh_per_second=10) as live:
                    for message_chunk, metadata in app.stream(
                        {"messages": [HumanMessage(content=user_input)]},
                        config={"configurable": {"thread_id": thread_id}},
                        stream_mode="messages"
                    ):
                        if hasattr(message_chunk, 'content') and message_chunk.content:
                            response_buffer += message_chunk.content
                            display_buffer += message_chunk.content
                            
                            # Update display every few characters or at natural breaks
                            if len(display_buffer) >= 20 or any(char in message_chunk.content for char in ['.', '!', '?', '\n']):
                                if is_likely_markdown(response_buffer):
                                    # Render as markdown
                                    try:
                                        markdown_content = Markdown(response_buffer)
                                        live.update(markdown_content)
                                    except:
                                        # Fallback to plain text if markdown parsing fails
                                        live.update(Text(response_buffer))
                                else:
                                    # Display as plain text
                                    live.update(Text(response_buffer))
                                
                                display_buffer = ""
                                time.sleep(0.05)  # Small delay for smooth streaming
                
                # Final render after streaming is complete
                if response_buffer:
                    console.print()  # New line
                    if is_likely_markdown(response_buffer):
                        final_markdown = Markdown(response_buffer)
                        console.print(final_markdown)
                    else:
                        console.print(response_buffer)
                        
            except Exception as stream_error:
                console.print(f"\n❌ [red]Streaming error:[/red] {stream_error}")
                continue
            
        except KeyboardInterrupt:
            console.print("\n\n🤖 [yellow]Chat interrupted. Goodbye![/yellow] 👋")
            break
        except Exception as e:
            console.print(f"\n❌ [red]Error:[/red] {e}")

if __name__ == "__main__":
    markdown_streaming_chat()
