from sdx_gcp.app import get_logger

from app import CONFIG, sdx_app
from app.output_type import OutputType

logger = get_logger()


dir_dict = {OutputType.DAP: "dap",
            OutputType.LEGACY: "survey",
            OutputType.HYBRID: "survey",
            OutputType.FEEDBACK: "feedback",
            OutputType.COMMENTS: "comments",
            OutputType.SEFT: "seft",
            OutputType.SPP: "survey"}


def write_to_bucket(data: str, filename: str, output_type: OutputType) -> str:
    """
    Uploads a string submission to the correct folder within the GCP outputs bucket.
    """
    logger.info("Uploading to bucket")
    directory = dir_dict.get(output_type)
    # remove destination suffix if it exists
    name = filename.split(":")[0]
    return sdx_app.gcs_write(data, name, CONFIG.BUCKET_NAME, directory)
