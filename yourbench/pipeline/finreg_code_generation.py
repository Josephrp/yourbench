from typing import Any, Dict

from loguru import logger

from yourbench.utils.prompts import FINREG_CODE_GEN_PROMPT
from yourbench.utils.dataset_engine import custom_load_dataset, custom_save_dataset
from yourbench.utils.inference_engine import InferenceCall, run_inference


def run(config: Dict[str, Any]) -> None:
    stage_cfg = config.get("pipeline", {}).get("finreg_code_generation", {})
    if not stage_cfg.get("run", False):
        logger.info("finreg_code_generation stage is disabled. Skipping.")
        return

    source_subset = stage_cfg.get("source_subset", "chunked")
    output_subset = stage_cfg.get("output_subset", "finreg_code")

    dataset = custom_load_dataset(config=config, subset=source_subset)
    if not dataset or len(dataset) == 0:
        logger.warning(f"No data found in subset '{source_subset}'. Skipping code generation.")
        return

    logger.info(f"Loaded {len(dataset)} documents for code generation.")

    calls = []
    for row in dataset:
        regulation_text = row.get("regulation_text", "")
        xml_code = row.get("xml_code", "")
        prompt = FINREG_CODE_GEN_PROMPT.format(regulation_text=regulation_text, xml_code=xml_code)
        calls.append(InferenceCall(messages=[{"role": "user", "content": prompt}], tags=["finreg_code_generation"]))

    responses_dict = run_inference(config=config, step_name="finreg_code_generation", inference_calls=calls)
    # Assume single model for simplicity
    model_name = next(iter(responses_dict), None)
    if not model_name:
        logger.error("No model responses received for code generation.")
        return
    responses = responses_dict[model_name]

    # Add generated code to dataset
    dataset = dataset.add_column("generated_code", responses)
    custom_save_dataset(dataset, config=config, subset=output_subset)
    logger.success(f"Saved code generation results to subset '{output_subset}'.")
