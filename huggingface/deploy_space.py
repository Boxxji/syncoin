#!/usr/bin/env python3
"""
SynCoin Hugging Face Space 1-Click Deployer
MIT License — 100% Free & Open-Source
"""
import os
import sys

try:
    from huggingface_hub import HfApi, create_repo, upload_folder
except ImportError:
    print("Please install huggingface_hub: pip install huggingface_hub")
    sys.exit(1)

def deploy(space_name: str = "syncoin-hub", token: str = None):
    token = token or os.environ.get("HF_TOKEN")
    if not token:
        print("❌ Error: No Hugging Face token provided.")
        print("Set HF_TOKEN in your environment or pass it as an argument:")
        print("python3 deploy_space.py --token hf_yourTokenHere --space your-username/syncoin-hub")
        sys.exit(1)

    api = HfApi(token=token)
    user = api.whoami()
    username = user["name"]
    full_repo_id = f"{username}/{space_name}" if "/" not in space_name else space_name

    print(f"🚀 Creating / Checking Hugging Face Space: {full_repo_id}...")
    try:
        create_repo(
            repo_id=full_repo_id,
            repo_type="space",
            space_sdk="docker",
            private=False,
            token=token,
            exist_ok=True
        )
        print(f"✅ Space created: https://huggingface.co/spaces/{full_repo_id}")
    except Exception as e:
        print(f"⚠️ Notice on repo creation: {e}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📦 Uploading template files from {current_dir} to {full_repo_id}...")
    
    upload_folder(
        folder_path=current_dir,
        repo_id=full_repo_id,
        repo_type="space",
        token=token,
        ignore_patterns=["deploy_space.py", "*.pyc", "__pycache__"]
    )
    print("🎉 DEPLOYMENT COMPLETE!")
    print(f"🌐 Your Public SynCoin Space is Live at: https://huggingface.co/spaces/{full_repo_id}")
    print(f"📡 WebSocket Worker Entrypoint: wss://{username}-{space_name.split('/')[-1]}.hf.space/ws")
    print(f"🔗 OpenAI REST Endpoint: https://{username}-{space_name.split('/')[-1]}.hf.space/v1/chat/completions")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Deploy SynCoin Hub to Hugging Face Spaces")
    parser.add_argument("--space", default="syncoin-hub", help="Space name (e.g. syncoin-hub)")
    parser.add_argument("--token", default=None, help="Hugging Face User Access Token (hf_...)")
    args = parser.parse_args()

    deploy(space_name=args.space, token=args.token)
