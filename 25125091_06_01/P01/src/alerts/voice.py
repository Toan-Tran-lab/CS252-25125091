"""Voice alert prompts and Web Speech API generators for SmartRoute.

Owner: Tran Duc Toan (25125091) - Group 06
Fulfills Week 08 task: Vietnamese browser voice alert for Simulate Drive.
"""

from __future__ import annotations

# Exact prompt specified in Task Division 2
POTHOLE_VOICE_ALERT_VI: str = (
    "Chú ý: Phía trước 50 mét có ổ gà ngập nước, vui lòng giảm tốc độ"
)


def get_pothole_voice_text(
    distance_m: int = 50, hazard_label: str = "ổ gà ngập nước"
) -> str:
    """Generate standardized Vietnamese voice alert text for lookahead warnings."""
    return f"Chú ý: Phía trước {distance_m} mét có {hazard_label}, vui lòng giảm tốc độ"


def generate_web_speech_script(
    text: str = POTHOLE_VOICE_ALERT_VI, rate: float = 1.05
) -> str:
    """Generate ready-to-inject JavaScript snippet using browser Web Speech API."""
    return f"""// Web Speech API Voice Synthesizer (Tiếng Việt)
function playPotholeVoiceAlert() {{
  if ('speechSynthesis' in window) {{
    try {{
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance({repr(text)});
      utterance.lang = 'vi-VN';
      utterance.rate = {rate};
      window.speechSynthesis.speak(utterance);
    }} catch (err) {{
      console.warn('Speech synthesis failed:', err);
    }}
  }}
}}"""
