import getpass
import os
import time
import asyncio
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import SystemMessage, HumanMessage

# Rich imports for animations
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.align import Align
from rich.layout import Layout
from rich.rule import Rule

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
        system_prompt = """You are an AI assistant that provides helpful responses with markdown formatting.
        Use formatting like **bold**, *italic*, `code`, lists, and headers to make responses visually appealing."""
        
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = model.invoke(messages)
        return {"messages": response}

    workflow.add_node("model", call_model)
    workflow.add_edge(START, "model")
    return workflow.compile(checkpointer=MemorySaver())

def typewriter_effect(console, text, delay=0.03, style=""):
    """Typewriter animation effect"""
    for i in range(len(text) + 1):
        console.clear()
        console.print(text[:i], style=style, end="")
        time.sleep(delay)

def animated_welcome(console):
    """Animated welcome screen"""
    console.clear()
    
    # Create animated title
    title_text = "🤖 LangChain Animated Chatbot 🚀"
    
    with console.status("[bold green]Initializing AI systems...") as status:
        time.sleep(1)
        status.update("[bold blue]Loading neural networks...")
        time.sleep(1)
        status.update("[bold cyan]Preparing markdown renderer...")
        time.sleep(1)
        status.update("[bold magenta]Starting conversation engine...")
        time.sleep(1)
    
    console.clear()
    
    # Typewriter effect for title
    typewriter_effect(console, title_text, 0.05, "bold cyan")
    
    # Animated panels
    features = [
        "✨ Real-time streaming",
        "🎨 Rich markdown rendering", 
        "🧠 Conversation memory",
        "🎭 Beautiful animations",
        "⚡ Smooth performance"
    ]
    
    console.print("\n" + "="*60)
    console.print("[bold yellow]Features:[/bold yellow]")
    
    for feature in features:
        console.print(f"  {feature}")
        time.sleep(0.3)
    
    console.print("="*60)
    console.print("[dim]Commands: 'quit', 'exit', 'bye' to end chat[/dim]")
    console.print()

def animated_thinking_spinner():
    """Create thinking animation"""
    return Spinner("dots12", text="AI is thinking...", style="cyan")

def animated_streaming_chat():
    """Main animated chatbot with Rich effects - FIXED duplicate issue"""
    console = Console()
    
    # Show animated welcome
    animated_welcome(console)
    
    app = create_chatbot_app()
    if not app:
        console.print("[red]❌ Failed to initialize chatbot[/red]")
        return
    
    thread_id = "animated_session_1"
    
    while True:
        try:
            # Animated input prompt
            input_panel = Panel(
                "[bold blue]Type your message below[/bold blue]",
                title="💬 Chat Input",
                border_style="blue"
            )
            console.print(input_panel)
            
            user_input = console.input("👤 [bold blue]You:[/bold blue] ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                # Animated goodbye
                goodbye_text = "🤖 Thank you for chatting! Goodbye! 👋"
                typewriter_effect(console, goodbye_text, 0.03, "bold green")
                console.print()
                break
            
            # Show thinking animation and stream response
            response_buffer = ""
            
            with console.status(animated_thinking_spinner()) as status:
                # Create animated response with Live display
                with Live(console=console, refresh_per_second=20, screen=False) as live:
                    for message_chunk, metadata in app.stream(
                        {"messages": [HumanMessage(content=user_input)]},
                        config={"configurable": {"thread_id": thread_id}},
                        stream_mode="messages"
                    ):
                        if hasattr(message_chunk, 'content') and message_chunk.content:
                            response_buffer += message_chunk.content
                            
                            # Create animated response panel
                            response_panel = Panel(
                                Markdown(response_buffer + "▋"),  # Cursor effect
                                title="🤖 AI Response",
                                border_style="green",
                                padding=(1, 2)
                            )
                            
                            live.update(response_panel)
                            time.sleep(0.05)  # Control animation speed
            
            # FIXED: Removed duplicate final response rendering
            # The Live display already shows the complete response
            
            # Add separator with animation
            console.print()
            console.print(Rule("[dim]Conversation continues...[/dim]", style="dim"))
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]💫 Chat gracefully interrupted. Goodbye![/yellow]")
            break
        except Exception as e:
            error_panel = Panel(
                f"[red]❌ Error: {e}[/red]",
                title="Error",
                border_style="red"
            )
            console.print(error_panel)

def progress_bar_demo(console):
    """Demo with progress bars for initialization"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        
        task1 = progress.add_task("[cyan]Loading LangChain...", total=100)
        task2 = progress.add_task("[green]Initializing AI model...", total=100)
        task3 = progress.add_task("[yellow]Setting up memory...", total=100)
        
        for i in range(100):
            progress.update(task1, advance=1)
            if i > 30:
                progress.update(task2, advance=1)
            if i > 60:
                progress.update(task3, advance=1)
            time.sleep(0.02)

async def async_animated_chat():
    """Async version with even smoother animations - FIXED duplicate issue"""
    console = Console()
    
    # Progress bar initialization
    progress_bar_demo(console)
    console.clear()
    
    # Animated welcome
    animated_welcome(console)
    
    app = create_chatbot_app()
    if not app:
        console.print("[red]❌ Failed to initialize chatbot[/red]")
        return
    
    thread_id = "async_animated_session"
    
    while True:
        try:
            user_input = console.input("\n👤 [bold blue]You:[/bold blue] ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                # Animated farewell
                farewell_table = Table(title="🎭 Chat Session Complete")
                farewell_table.add_column("Metric", style="cyan")
                farewell_table.add_column("Status", style="green")
                farewell_table.add_row("Session", "✅ Successful")
                farewell_table.add_row("Memory", "💾 Preserved")
                farewell_table.add_row("Experience", "⭐ Excellent")
                
                console.print(farewell_table)
                console.print("\n[bold green]🤖 Thank you for the amazing conversation! 🚀[/bold green]")
                break
            
            # Animated response generation
            response_text = ""
            
            with Live(console=console, refresh_per_second=30) as live:
                async for message_chunk, metadata in app.astream(
                    {"messages": [HumanMessage(content=user_input)]},
                    config={"configurable": {"thread_id": thread_id}},
                    stream_mode="messages"
                ):
                    if hasattr(message_chunk, 'content') and message_chunk.content:
                        response_text += message_chunk.content
                        
                        # Create pulsing border effect
                        colors = ["green", "cyan", "blue", "magenta"]
                        color = colors[len(response_text) % len(colors)]
                        
                        animated_panel = Panel(
                            Markdown(response_text + " ⚡"),
                            title=f"🤖 AI Response {['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'][len(response_text) % 10]}",
                            border_style=color,
                            padding=(1, 2)
                        )
                        
                        live.update(animated_panel)
                        await asyncio.sleep(0.03)
            
            # FIXED: Removed duplicate final response rendering
            # The Live display already shows the complete response
            
        except KeyboardInterrupt:
            console.print("\n[rainbow]🌈 Until next time! 👋[/rainbow]")
            break
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")

def main():
    """Choose between sync and async versions"""
    console = Console()
    
    choice_table = Table(title="🎭 Choose Your Animation Experience")
    choice_table.add_column("Option", style="cyan")
    choice_table.add_column("Description", style="white")
    choice_table.add_row("1", "🎬 Standard Animated Chat")
    choice_table.add_row("2", "🚀 Ultra-Smooth Async Chat")
    
    console.print(choice_table)
    
    choice = console.input("\n[bold yellow]Choose (1 or 2):[/bold yellow] ").strip()
    
    if choice == "2":
        asyncio.run(async_animated_chat())
    else:
        animated_streaming_chat()

if __name__ == "__main__":
    main()
