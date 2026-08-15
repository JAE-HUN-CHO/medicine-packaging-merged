"""v3 RF-DETR Medium hosted inference.

Needs a Roboflow API key and workspace credits.
Model: medicine-packaging-merged-v2/3
"""

from __future__ import annotations

import os
import sys

MODEL_ID = "medicine-packaging-merged-v2/3"


def main() -> None:
    image = sys.argv[1] if len(sys.argv) > 1 else None
    if not image:
        raise SystemExit("usage: python examples/infer.py <image-url-or-path>")

    from inference_sdk import InferenceHTTPClient

    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key=os.environ["ROBOFLOW_API_KEY"],
    )
    result = client.infer(image, model_id=MODEL_ID)
    for pred in result.get("predictions", []):
        print(f"{pred['class']:20s}  {pred['confidence']:.2f}")


if __name__ == "__main__":
    main()
