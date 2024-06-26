import json
from pytorch_lightning import Trainer
from pytorch_lightning import seed_everything
import hydra
from omegaconf import OmegaConf, DictConfig

from src.pipelines.pipeline import train, predict, tune


@hydra.main(config_path="configs/", config_name="resnet.yaml")
def main(
    config: DictConfig,
) -> None:
    if config.is_tuned == "tuned":
        params = json.load(open(config.tuned_hparams_path, "rt", encoding="UTF-8"))
        config = OmegaConf.merge(config, params)
    elif config.is_tuned == "untuned":
        pass
    else:
        raise ValueError(f"Invalid is_tuned argument: {config.is_tuned}")

    if config.mode == "train":
        return train(config)
    elif config.mode == "predict":
        return predict(config)
    elif config.mode == "tune":
        return tune(config)
    else:
        raise ValueError(f"Invalid execution mode: {config.mode}")


if __name__ == "__main__":
    main()
