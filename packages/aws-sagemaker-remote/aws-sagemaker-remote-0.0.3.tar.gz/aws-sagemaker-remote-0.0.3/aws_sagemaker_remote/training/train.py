from ..session import sagemaker_session
from .config import SageMakerTrainingConfig
import os
from sagemaker.pytorch import PyTorch
from .channels import standardize_channels, upload_local_channels
from sagemaker.utils import name_from_base
from .iam import ensure_training_role

CHECKPOINT_LOCAL_PATH = '/opt/ml/checkpoints'


def sagemaker_training_run(
    args,
    config: SageMakerTrainingConfig,
    metrics=None
):
    if metrics is None:
        metrics = {}
    session = sagemaker_session(
        profile_name=args.sagemaker_profile
    )
    script = args.sagemaker_script
    script = os.path.abspath(script)
    source = args.sagemaker_source
    if not source:
        source = os.path.dirname(script)
    if not script.startswith(source):
        raise ValueError("script=[{}] must be in source=[{}]")
    entry_point = script[len(source)+1:]
    entry_point = entry_point.replace("\\","/")
    metric_definitions = [
        {'Name': k, 'Regex': v}
        for k, v in metrics.items()
    ]
    dependencies = [getattr(args, k) for k in config.dependencies.keys()]

    # checkpoint_local_path='/opt/ml/checkpoints/'
    bucket = session.default_bucket()
    if args.sagemaker_job_name and len(args.sagemaker_job_name.strip()) > 0:
        job_name = args.sagemaker_job_name
    else:
        job_name = name_from_base(args.sagemaker_base_job_name)
    #checkpoint_s3_uri = 's3://{}/{}/checkpoints'.format(bucket, job_name)
    input_prefix = "s3://{}/{}/inputs".format(bucket, job_name)
    iam = session.boto_session.client('iam')
    training_role = ensure_training_role(
        iam=iam, role_name=args.sagemaker_training_role)
    estimator = PyTorch(
        sagemaker_session=session,
        base_job_name=args.sagemaker_base_job_name,
        entry_point=entry_point,
        source_dir=source,
        role=training_role,
        instance_type=args.sagemaker_training_instance,
        image_uri=args.sagemaker_training_image,
        instance_count=1,
        framework_version='1.5.0',
        # hyperparameters=hyperparameters_from_argparse(vars(args)),
        metric_definitions=metric_definitions,
        dependencies=dependencies,
        # checkpoint_s3_uri=checkpoint_s3_uri,
        checkpoint_local_path=CHECKPOINT_LOCAL_PATH
    )

    channels = config.channels
    channels = standardize_channels(channels=channels)
    channels = upload_local_channels(
        channels=channels, session=session, prefix=input_prefix)

    estimator.fit(channels, job_name=job_name, wait=args.sagemaker_wait)
    # todo:
    # use_spot_instances
    # experiment_config (dict[str, str]): Experiment management configuration.
    #            Dictionary contains three optional keys,
    #            'ExperimentName', 'TrialName', and 'TrialComponentDisplayName'.
    return estimator
