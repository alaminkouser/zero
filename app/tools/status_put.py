from pydantic import BaseModel
import subprocess


class StatusPutInput(BaseModel):
    status: str


class StatusPutOutput(BaseModel):
    ok: bool


def status_put(input: StatusPutInput) -> StatusPutOutput:
    """
    Updates the personal status message displayed on the website.

    Use this tool to share a short, human-readable update about the current
    personal situation (e.g., availability, focus, mood, or ongoing
    activities) on https://alaminkouser.com/status/.

    The input should be concise and clear, such as "Working deeply, limited
    availability", "Taking a break", or "Open to new opportunities". Avoid
    sensitive or overly detailed personal information. Keep messages brief,
    intentional, and appropriate for public visibility.
    """
    try:
        subprocess.run(["status-put", input.status])
        return StatusPutOutput(ok=True)
    except Exception as e:
        print(e)
        return StatusPutOutput(ok=False)
