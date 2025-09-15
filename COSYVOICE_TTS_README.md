# CosyVoice TTS Implementation

This project uses the CosyVoice TTS model from ModelScope for cross-platform compatibility. It replaces the previous macOS-specific TTS implementation with a more universal solution.

## Features

- Cross-platform compatibility (Windows, Linux, macOS)
- Local deployment without internet connection
- Support for multiple voice types
- Fallback to placeholder audio generation if model loading fails

## Dependencies

The CosyVoice TTS implementation requires the following dependencies:

- modelscope>=1.29.2
- cosyvoice>=0.0.5
- torch>=2.8.0
- torchaudio>=2.8.0
- transformers>=4.56.1
- peft>=0.17.1
- diffusers>=0.35.1

## Usage

The CosyVoiceTTS class can be used as follows:

```python
from cosyvoice_tts import CosyVoiceTTS

# Create TTS instance
tts = CosyVoiceTTS(voice="中文女")

# Generate speech from text
output_path = tts.speak_to_file("你好，世界！", "output.wav")
```

## Voice Types

Currently supported voice types:
- 中文女 (Chinese Female)
- 中文男 (Chinese Male)
- 英文女 (English Female)
- 英文男 (English Male)

## Implementation Details

The implementation automatically handles:
1. Model downloading from ModelScope
2. Model loading and initialization
3. Audio generation with proper formatting
4. Fallback to placeholder audio if model loading fails

The placeholder implementation generates simple sine wave audio as a fallback mechanism.