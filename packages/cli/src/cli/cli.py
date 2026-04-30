"""CLI using Typer."""

# CLI for exercise notebook
# import typer

# app = typer.Typer(
#     name="CLI using Typer"
# )

# @app.command()
# def say_hi(name):
#     """Say hello to the user."""
#     typer.echo(f"Hello: {name}")

# @app.command()
# def goodbye():
#     """Say goodbye to the user."""
#     typer.echo("Goodbye!")

# @app.callback()
# def welcome():
#     """Print a welcome message to the user."""
#     print("Welcome!")

# if __name__ == "__main__":
#     app()


# CLI for hackathon
# Skeleton for a CLI

import logging
from pathlib import Path

import typer

from animal_shelter.data import load_data
from animal_shelter.features import add_features
from animal_shelter.model import train_model, save_model, predict_with_model

import pandas as pd

app = typer.Typer()

# Always gets called before all subcommands
@app.callback()
def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)-15s] %(name)s - %(levelname)s - %(message)s",
    )


@app.command()
def train(input_path: Path, model_path: Path) -> None:
    """Trains a model on the given dataset."""
    typer.echo(f"Loading {input_path}")
    logger = logging.getLogger(__name__)
    logger.info("Loading input dataset from %s", input_path)
    
    # Load/process data
    animal_outcomes = load_data(input_path)
    logger.debug("Loaded dataset with %d rows and %d columns", animal_outcomes.shape[0], animal_outcomes.shape[1])
        
    # Pass data to functions from animal_shelter
    with_features = add_features(animal_outcomes)
    logger.debug("Added features, resulting dataset has %d rows and %d columns", with_features.shape[0], with_features.shape[1])
    logger.info("All train data loaded")

    # Train and save the model
    logger.info("Start training model")
    model, metrics = train_model(with_features)
    logger.info("Finished training model with metrics: %s", metrics)
    save_model(model, model_path)
    logger.info("Model saved to %s", model_path)

    # Check that the model is saved correctly
    if model_path.is_file():
        logger.info("Model is saved correctly at %s", model_path)
    else:
        raise FileNotFoundError("Model is not saved")
    
    # Output some useful feedback for the user: accuracy, number of samples, number of features
    typer.echo(f"Model saved to: {model_path}")
    typer.echo(f"Accuracy: {metrics['accuracy']:.4f}")
    typer.echo(f"Number of samples: {metrics['n_samples']}")
    typer.echo(f"Number of features: {metrics['n_features']}")
    
@app.command()
def predict(input_path: Path, model_path: Path, output_path: Path) -> None:
    """Applies a model to the given dataset."""
    typer.echo(f"Loading {input_path}")

    logger = logging.getLogger(__name__)

    # Load/process data
    animal_outcomes = load_data(input_path)
    logger.debug("Loaded test dataset with %d rows and %d columns", animal_outcomes.shape[0], animal_outcomes.shape[1])
        
    # Pass data to functions from animal_shelter
    with_features = add_features(animal_outcomes)
    logger.debug("Added features, resulting dataset has %d rows and %d columns", with_features.shape[0], with_features.shape[1])
    logger.info("All test data loaded")

    # Generate predictions by calling functions from animal_shelter
    pred_df = predict_with_model(model_path, with_features)

    # Format predictions
    pred_summary = pred_df.groupby('prediction').size().reset_index()
    for i in range(len(pred_summary)):
        pred_class = pred_summary.loc[i]
        pred_class_percent = round(pred_class[0] / len(pred_df) * 100,2)
        typer.echo(f"{pred_class['prediction']:20s}: {pred_class[0]} animals ({pred_class_percent}%)")

    # Add max probability column
    proba_cols = ["proba_Adoption", "proba_Died", "proba_Euthanasia", "proba_Return_to_owner", "proba_Transfer"]
    pred_df["prediction_probability"] = pred_df[proba_cols].max(axis=1)

    result = pd.concat([with_features[["id", "name", "breed", "color", "days_upon_outcome"]], pred_df[['prediction', 'prediction_probability']]], axis=1)
    typer.echo("Sample output:")
    typer.echo(result.head(5).to_string(index=False))

    # Save/return predictions and some useful feedback for the user
    result.to_csv(output_path, index=False)
    typer.echo(f"Predictions saved to: {output_path}")
