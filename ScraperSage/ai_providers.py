"""
AI Provider configurations and handlers for ScraperSage.
Supports single provider selection: Gemini, OpenAI, OpenRouter, or DeepSeek.
Models must be explicitly specified by the user.
"""

import os
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential


class AIProvider:
    """Base class for AI providers."""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.provider_name = self.__class__.__name__.replace("Provider", "").lower()
    
    def generate_summary(self, content: str, query: str) -> str:
        """Generate summary using the AI provider."""
        raise NotImplementedError
    
    def validate_model(self, model: str) -> bool:
        """Validate if model is supported by the provider."""
        return True  # Default implementation accepts any model


class GeminiProvider(AIProvider):
    """Google Gemini AI provider with explicit model requirement."""
    
    def __init__(self, api_key: str, model: str):
        if not model:
            raise ValueError("Model is required for Gemini provider. Please specify a model like 'gemini-1.5-flash'.")
        
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        
        # Validate model by attempting to create the client
        try:
            self.client = genai.GenerativeModel(model)
        except Exception as e:
            raise ValueError(f"Invalid Gemini model '{model}': {str(e)}")
    
    def validate_model(self, model: str) -> bool:
        """Validate Gemini model by attempting to create client."""
        try:
            genai.GenerativeModel(model)
            return True
        except Exception:
            return False
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_summary(self, content: str, query: str) -> str:
        """Generate summary using Gemini."""
        prompt = f"""
        Based on the following content related to "{query}", provide a comprehensive and informative summary:
        
        Content: {content[:4000]}
        
        Please provide a clear, concise summary that captures the key points and insights relevant to the query.
        Focus on the most important information and main themes.
        """
        
        try:
            response = self.client.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Summary generation failed: {str(e)}"


class OpenAIProvider(AIProvider):
    """OpenAI provider with explicit model requirement."""
    
    def __init__(self, api_key: str, model: str):
        if not model:
            raise ValueError("Model is required for OpenAI provider. Please specify a model like 'gpt-4o-mini'.")
            
        super().__init__(api_key, model)
        self.client = OpenAI(api_key=api_key)
        
        # Note: OpenAI doesn't provide model validation endpoint, so we'll validate on first use
    
    def validate_model(self, model: str) -> bool:
        """Basic validation for OpenAI models."""
        # Basic check for common OpenAI model patterns
        common_patterns = ["gpt-", "text-", "davinci", "curie", "babbage", "ada"]
        return any(pattern in model.lower() for pattern in common_patterns)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_summary(self, content: str, query: str) -> str:
        """Generate summary using OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates comprehensive summaries of web content."
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Based on the following content related to "{query}", provide a comprehensive and informative summary:
                        
                        Content: {content[:4000]}
                        
                        Please provide a clear, concise summary that captures the key points and insights relevant to the query.
                        Focus on the most important information and main themes.
                        """
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Summary generation failed: {str(e)}"


class OpenRouterProvider(AIProvider):
    """OpenRouter provider with explicit model requirement."""
    
    def __init__(self, api_key: str, model: str):
        if not model:
            raise ValueError("Model is required for OpenRouter provider. Please specify a model like 'openai/gpt-4o-mini'.")
            
        super().__init__(api_key, model)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
    
    def validate_model(self, model: str) -> bool:
        """Basic validation for OpenRouter models."""
        # OpenRouter models typically have provider/model format
        return "/" in model and len(model.split("/")) >= 2
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_summary(self, content: str, query: str) -> str:
        """Generate summary using OpenRouter."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates comprehensive summaries of web content."
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Based on the following content related to "{query}", provide a comprehensive and informative summary:
                        
                        Content: {content[:4000]}
                        
                        Please provide a clear, concise summary that captures the key points and insights relevant to the query.
                        Focus on the most important information and main themes.
                        """
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Summary generation failed: {str(e)}"


class DeepSeekProvider(AIProvider):
    """DeepSeek provider with explicit model requirement."""
    
    def __init__(self, api_key: str, model: str):
        if not model:
            raise ValueError("Model is required for DeepSeek provider. Please specify a model like 'deepseek-chat'.")
            
        super().__init__(api_key, model)
        self.client = OpenAI(
            base_url="https://api.deepseek.com",
            api_key=api_key
        )
    
    def validate_model(self, model: str) -> bool:
        """Basic validation for DeepSeek models."""
        # DeepSeek models typically start with "deepseek-"
        return model.startswith("deepseek-") or model in ["deepseek-chat", "deepseek-coder"]
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_summary(self, content: str, query: str) -> str:
        """Generate summary using DeepSeek."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates comprehensive summaries of web content."
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Based on the following content related to "{query}", provide a comprehensive and informative summary:
                        
                        Content: {content[:4000]}
                        
                        Please provide a clear, concise summary that captures the key points and insights relevant to the query.
                        Focus on the most important information and main themes.
                        """
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Summary generation failed: {str(e)}"


def create_ai_provider(provider: str, api_key: str = None, model: str = None) -> AIProvider:
    """Create a single AI provider instance with explicit model requirement."""
    
    # Provider class mapping
    providers = {
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
        "openrouter": OpenRouterProvider,
        "deepseek": DeepSeekProvider
    }
    
    if provider not in providers:
        raise ValueError(f"Unsupported provider: {provider}. Available: {list(providers.keys())}")
    
    if not model:
        raise ValueError(f"Model is required. Please specify a model for {provider} provider.")
    
    # Get API key from environment if not provided
    if not api_key:
        env_keys = {
            "gemini": "GEMINI_API_KEY",
            "openai": "OPENAI_API_KEY",
            "openrouter": "OPENROUTER_API_KEY", 
            "deepseek": "DEEPSEEK_API_KEY"
        }
        
        env_key = env_keys[provider]
        api_key = os.getenv(env_key)
        
        if not api_key:
            raise ValueError(f"API key not found. Please set {env_key} environment variable or provide explicit key.")
    
    # Create provider instance (model validation happens in constructor)
    provider_class = providers[provider]
    return provider_class(api_key, model)


def get_supported_providers() -> List[str]:
    """Get list of supported providers."""
    return ["gemini", "openai", "openrouter", "deepseek"]


def get_available_models(provider: str) -> Dict[str, str]:
    """Get available models for a provider (returns empty - models must be specified explicitly)."""
    return {}
    example_models = {
        "gemini": {
            "gemini-1.5-flash": "Fast and efficient",
            "gemini-1.5-pro": "Most capable model",
            "gemini-1.0-pro": "Original Gemini model"
        },
        "openai": {
            "gpt-4o-mini": "Faster and cost-effective",
            "gpt-4o": "Latest and most capable",
            "gpt-4-turbo": "High performance",
            "gpt-3.5-turbo": "Cost-effective option"
        },
        "openrouter": {
            "openai/gpt-4o-mini": "GPT-4o mini via OpenRouter",
            "anthropic/claude-3.5-sonnet": "Anthropic's latest",
            "anthropic/claude-3-haiku": "Fast Anthropic model",
            "meta-llama/llama-3.1-8b-instruct": "Meta's Llama"
        },
        "deepseek": {
            "deepseek-chat": "General purpose",
            "deepseek-coder": "Optimized for code"
        }
    }
    
    return example_models.get(provider, {})


def get_default_model(provider: str) -> str:
    """Get default model for a provider."""
    defaults = {
        "gemini": "gemini-1.5-flash",
        "openai": "gpt-4o-mini",
        "openrouter": "openai/gpt-4o-mini",
        "deepseek": "deepseek-chat"
    }
    
    return defaults.get(provider, "")
