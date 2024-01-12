from pipelines.svd_film import StableVideoDiffusionFILMPipeline
from PIL import PngImagePlugin
import time
import torch

LARGE_ENOUGH_NUMBER = 100
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024**2)


def main():
    svd_config = {"sfast": True, "quantize": False, "no_fusion": False}
    pipeline = StableVideoDiffusionFILMPipeline(
        cache_dir="./cache", svd_config=svd_config
    )

    if svd_config["sfast"]:
        # Warm up
        begin = time.time()
        pipeline(output_path=None, image="test.png", inter_frames=0)
        end = time.time()

        print(f"warm up time: {end - begin:.3f}s")

    image = ["input/svd_kitten_init.png"]

    runs = 1

    run_times = []
    for _ in range(runs):
        begin = time.time()
        pipeline(output_path="output", image=image)
        end = time.time()

        run_times.append(end - begin)

    for idx, run_time in enumerate(run_times):
        print(f"run time {idx}: {run_time:.3f}s")

    peak_mem_allocated = torch.cuda.max_memory_allocated()
    peak_mem_reserved = torch.cuda.max_memory_reserved()
    print(f"peak GPU memory allocated: {peak_mem_allocated / 1024**3:.3f}GiB")
    print(f"peak GPU memory reserved: {peak_mem_reserved / 1024**3:.3f}GiB")


if __name__ == "__main__":
    main()
