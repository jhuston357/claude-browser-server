import os
import json
import time
import asyncio
import getpass
from typing import Dict, List, Optional, Union, Any
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# Models for API requests and responses
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 4096
    stream: Optional[bool] = False

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

class ConfigModel(BaseModel):
    email: str
    password: str
    headless: bool = True

# Global variables
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
config = None
browser = None
context = None
page = None
is_logged_in = False

# Create FastAPI app
app = FastAPI(title="Claude Browser API Server for OpenHands")

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_config():
    global config
    if config is None:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
        else:
            raise HTTPException(status_code=500, detail="Configuration not found. Please restart the server.")
    return config

async def initialize_browser():
    global browser, context, page, is_logged_in
    
    config_data = get_config()
    
    # Check if we're in demo mode
    if config_data.get("demo_mode", False):
        print("Running in demo mode. No browser will be initialized.")
        is_logged_in = True
        return None
    
    if browser is None:
        headless = config_data.get("headless", False)  # Default to visible browser for authentication
        
        print("Initializing browser...")
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Check if we need to log in
        if not is_logged_in:
            await login(config_data["email"], config_data.get("auth_method", "manual"))
    
    return page

async def login(email: str, auth_method: str = "manual"):
    global is_logged_in, page
    
    if page is None:
        raise HTTPException(status_code=500, detail="Browser not initialized")
    
    try:
        print("Logging into Claude...")
        await page.goto("https://claude.ai/login")
        
        # Wait for the login page to load
        await page.wait_for_selector('input[type="email"]', timeout=30000)
        
        # Enter email
        await page.fill('input[type="email"]', email)
        await page.click('button[type="submit"]')
        
        # At this point, Claude.ai will either:
        # 1. Send a verification code to the email
        # 2. Offer Google/other third-party login options
        
        if auth_method == "manual":
            # Pause for manual authentication
            print("\n==================================================")
            print(f"MANUAL AUTHENTICATION REQUIRED FOR: {email}")
            print("Please check your email for a verification code or complete the authentication in the browser.")
            print("The server will wait for you to complete the login process.")
            print("==================================================\n")
            
            # Wait for the chat page to load, which indicates successful login
            await page.wait_for_selector('div[data-testid="conversation-turn"], div[data-testid="new-chat-button"]', timeout=300000)  # 5 minutes timeout
            
            print("Successfully logged into Claude!")
            is_logged_in = True
        elif auth_method == "verification_code":
            # Wait for the verification code input field
            try:
                await page.wait_for_selector('input[type="text"][inputmode="numeric"]', timeout=30000)
                
                print("\n==================================================")
                print(f"VERIFICATION CODE REQUIRED FOR: {email}")
                print("Please check your email for a verification code and enter it below.")
                
                # For Docker: Check if there's a verification code file
                verification_code_file = "/tmp/verification_code.txt"
                if os.path.exists(verification_code_file):
                    with open(verification_code_file, "r") as f:
                        verification_code = f.read().strip()
                    # Remove the file after reading
                    os.remove(verification_code_file)
                    print(f"Using verification code from file: {verification_code}")
                else:
                    verification_code = input("Verification Code: ").strip()
                
                print("==================================================\n")
                
                # Enter the verification code
                await page.fill('input[type="text"][inputmode="numeric"]', verification_code)
                await page.click('button[type="submit"]')
                
                # Wait for the chat page to load, which indicates successful login
                await page.wait_for_selector('div[data-testid="conversation-turn"], div[data-testid="new-chat-button"]', timeout=60000)
                
                print("Successfully logged into Claude!")
                is_logged_in = True
            except Exception as e:
                print(f"Verification code entry failed: {str(e)}")
                print("Falling back to manual authentication...")
                
                print("\n==================================================")
                print("MANUAL AUTHENTICATION FALLBACK")
                print("Please complete the authentication in the browser (if visible)")
                print("or check your email for alternative login methods.")
                print("The server will wait for you to complete the login process.")
                print("==================================================\n")
                
                # Wait for the chat page to load, which indicates successful login
                await page.wait_for_selector('div[data-testid="conversation-turn"], div[data-testid="new-chat-button"]', timeout=300000)  # 5 minutes timeout
                
                print("Successfully logged into Claude!")
                is_logged_in = True
        else:
            # This would be for future implementation of other automated authentication methods
            raise HTTPException(status_code=501, detail="Unsupported authentication method")
    except Exception as e:
        print(f"Login failed: {str(e)}")
        is_logged_in = False
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")

async def send_message_to_claude(message: str, system_prompt: Optional[str] = None):
    global page, is_logged_in
    
    # Check if we're in demo mode
    config_data = get_config()
    if config_data.get("demo_mode", False):
        print(f"Demo mode: Received message: {message}")
        if system_prompt:
            print(f"Demo mode: System prompt: {system_prompt}")
        
        # Generate a mock response
        if "hello" in message.lower() or "hi" in message.lower():
            return "Hello! I'm Claude (demo mode). How can I help you today?"
        elif "who are you" in message.lower() or "what are you" in message.lower():
            return "I'm Claude, an AI assistant created by Anthropic. This is a demo mode response."
        elif "weather" in message.lower():
            return "I don't have access to real-time weather data in this demo mode. In actual use, I would be able to provide more helpful information."
        else:
            return f"This is a demo response to your message: '{message}'. In actual use with real Claude credentials, you would receive a genuine response from Claude."
    
    # Real mode with browser automation
    if not is_logged_in or page is None:
        page = await initialize_browser()
    
    try:
        # Navigate to a new chat
        await page.goto("https://claude.ai/chats")
        await page.wait_for_selector('button[aria-label="New chat"]', timeout=30000)
        await page.click('button[aria-label="New chat"]')
        
        # Wait for the chat input to be ready
        await page.wait_for_selector('div[data-testid="chat-input-box"]', timeout=30000)
        
        # If there's a system prompt, set it first
        if system_prompt:
            # Open the settings
            await page.click('button[aria-label="Chat settings"]')
            
            # Wait for the settings panel
            await page.wait_for_selector('textarea[placeholder="Add custom instructions"]', timeout=10000)
            
            # Enter system prompt
            await page.fill('textarea[placeholder="Add custom instructions"]', system_prompt)
            
            # Save settings
            await page.click('button[aria-label="Save custom instructions"]')
            
            # Wait for settings to be saved
            await page.wait_for_timeout(1000)
        
        # Type the message
        await page.fill('div[data-testid="chat-input-box"]', message)
        
        # Send the message
        await page.click('button[data-testid="send-message-button"]')
        
        # Wait for Claude to respond
        response_selector = 'div[data-testid="conversation-turn-2"] div[data-message-author-role="assistant"]'
        await page.wait_for_selector(response_selector, timeout=60000)
        
        # Get the response text
        response_text = await page.text_content(response_selector)
        
        return response_text.strip()
    except Exception as e:
        print(f"Error sending message to Claude: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error communicating with Claude: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Claude Browser API Server for OpenHands is running"}

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest, background_tasks: BackgroundTasks):
    try:
        # Extract the last user message and any system message
        user_message = None
        system_message = None
        
        for msg in request.messages:
            if msg.role == "user":
                user_message = msg.content
            elif msg.role == "system":
                system_message = msg.content
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found in the request")
        
        # Send the message to Claude and get the response
        response_text = await send_message_to_claude(user_message, system_message)
        
        # Create a response in the format expected by OpenHands
        return {
            "id": f"claude-browser-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(user_message) // 4,  # Rough estimate
                "completion_tokens": len(response_text) // 4,  # Rough estimate
                "total_tokens": (len(user_message) + len(response_text)) // 4  # Rough estimate
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def setup_config():
    """Prompt for configuration values and save to config file"""
    global config
    
    print("\n=== Claude Browser API Server Configuration ===")
    
    print("Do you want to run in demo mode? (y/n, default: n):")
    demo_mode = input().strip().lower() == "y"
    
    if demo_mode:
        print("Running in demo mode. No actual browser automation will occur.")
        email = "demo@example.com"
        auth_method = "manual"
        headless = True
    else:
        print("Please enter your Claude.ai email:")
        email = input().strip()
        
        print("\nChoose authentication method:")
        print("1. verification_code - Enter verification code via terminal (good for SSH/headless servers)")
        print("2. manual - Complete authentication in browser window (default)")
        auth_choice = input("Enter choice (1/2): ").strip()
        
        if auth_choice == "1":
            auth_method = "verification_code"
            print("\nNOTE: With 'verification_code' authentication:")
            print("- You'll be prompted to enter the verification code in the terminal")
            print("- Check your email for the code when prompted")
            print("- Headless mode is fine since you don't need to see the browser")
        else:
            auth_method = "manual"
            print("\nNOTE: With 'manual' authentication, you'll need to:")
            print("- Complete the verification process in the browser window")
            print("- This may involve checking your email for a verification code")
            print("- Or using a third-party login option like Google")
            print("The server will wait for you to complete this process.")
        
        print("\nRun browser in headless mode? (y/n):")
        if auth_method == "verification_code":
            print("(For verification_code auth, either option works - default: y)")
            headless_input = input().strip().lower()
            headless = headless_input != "n"  # Default to headless for verification_code
        else:
            print("(For manual auth, visible browser is recommended - default: n)")
            headless_input = input().strip().lower()
            headless = headless_input == "y"  # Default to visible browser for manual authentication
    
    config = {
        "email": email,
        "auth_method": auth_method,
        "headless": headless,
        "demo_mode": demo_mode
    }
    
    # Save config to file
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)
    
    print(f"Configuration saved to {CONFIG_PATH}")

@app.on_event("startup")
async def startup_event():
    # Initialize the browser on startup if not in demo mode
    config_data = get_config()
    if not config_data.get("demo_mode", False):
        await initialize_browser()
    else:
        print("Starting in demo mode - no browser will be initialized")
        global is_logged_in
        is_logged_in = True

@app.on_event("shutdown")
async def shutdown_event():
    # Close the browser on shutdown if not in demo mode
    config_data = get_config()
    if not config_data.get("demo_mode", False):
        global browser
        if browser:
            await browser.close()

def main():
    # Check if config exists, if not, prompt for it
    if not os.path.exists(CONFIG_PATH):
        setup_config()
    
    # Start the server
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=54402,
        reload=True
    )

if __name__ == "__main__":
    main()