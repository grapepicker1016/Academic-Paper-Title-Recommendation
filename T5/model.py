from simpletransformers.t5 import T5Model

def get_base_model_args():
    return {
        "reprocess_input_data": True,
        "overwrite_output_dir": True,
        "max_seq_length": 256,
        "eval_batch_size": 128,
        "num_train_epochs": 1,
        "save_eval_checkpoints": False,
        "use_multiprocessing": False,
        "num_beams": None,
        "do_sample": True,
        "max_length": 50,
        "top_k": 50,
        "top_p": 0.95,
        "num_return_sequences": 3,
    }

def get_train_model_args(args):
    return {
        "max_seq_length": args.max_seq_length,
        "train_batch_size": args.train_batch_size,
        "num_train_epochs": args.epochs,
        "best_model_dir": args.best_model_dir,
        "output_dir": args.output_dir,
    }

def create_model(model_path, use_cuda=False, args=None):
    model_args = get_base_model_args()
    if args:
        model_args.update(get_train_model_args(args))
    return T5Model("t5", model_path, args=model_args, use_cuda=use_cuda)
