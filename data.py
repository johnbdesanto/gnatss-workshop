"""
Script to zip the data directory into a zip file using Typer CLI.
"""

import os
import zipfile
from pathlib import Path
from typing import Optional

import typer
from github import Github
from github.GithubException import GithubException


def zip_directory(source_dir, output_filename, verbose=True):
    """
    Zip a directory and all its contents with optional verbose output.
    
    Args:
        source_dir (str or Path): Path to the directory to zip
        output_filename (str or Path): Name of the output zip file
        verbose (bool): Whether to print verbose output
    """
    source_path = Path(source_dir)
    output_path = Path(output_filename)
    
    # Check if source directory exists
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory '{source_path}' does not exist")
    
    if not source_path.is_dir():
        raise NotADirectoryError(f"'{source_path}' is not a directory")
    
    if verbose:
        print(f"Creating zip archive: {output_path}")
        print(f"Source directory: {source_path}")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through all files and directories in source_dir
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = Path(root) / file
                # Calculate the archive name (relative path from source_dir)
                arcname = file_path.relative_to(source_path.parent)
                if verbose:
                    print(f"Adding: {arcname}")
                zipf.write(file_path, arcname)
    
    if verbose:
        print(f"Successfully created zip file: {output_path}")
        print(f"Zip file size: {output_path.stat().st_size:,} bytes")


def unzip_archive(zip_file, extract_to, verbose=True):
    """
    Unzip an archive to a specified directory.
    
    Args:
        zip_file (str or Path): Path to the zip file to extract
        extract_to (str or Path): Directory to extract files to
        verbose (bool): Whether to print verbose output
    """
    zip_path = Path(zip_file)
    extract_path = Path(extract_to)
    
    # Check if zip file exists
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file '{zip_path}' does not exist")
    
    if not zip_path.is_file():
        raise ValueError(f"'{zip_path}' is not a file")
    
    # Create extraction directory if it doesn't exist
    extract_path.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        print(f"Extracting zip archive: {zip_path}")
        print(f"Destination directory: {extract_path}")
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        # Get list of files in the archive
        file_list = zipf.namelist()
        
        if verbose:
            print(f"Found {len(file_list)} files in archive")
        
        # Extract all files
        for file_info in zipf.infolist():
            if verbose:
                print(f"Extracting: {file_info.filename}")
            zipf.extract(file_info, extract_path)
    
    if verbose:
        print(f"Successfully extracted {len(file_list)} files to: {extract_path}")


def create_github_release(
    repo_name: str,
    tag_name: str,
    release_name: str,
    release_notes: str,
    zip_file_path: Path,
    github_token: str,
    verbose: bool = True
):
    """
    Create a GitHub release and upload a zip file as an asset.
    
    Args:
        repo_name (str): Repository name in format "owner/repo"
        tag_name (str): Git tag name for the release
        release_name (str): Display name for the release
        release_notes (str): Description/notes for the release
        zip_file_path (Path): Path to the zip file to upload as asset
        github_token (str): GitHub personal access token
        verbose (bool): Whether to print verbose output
    """
    if verbose:
        print(f"Creating GitHub release for repository: {repo_name}")
        print(f"Tag: {tag_name}")
        print(f"Release name: {release_name}")
    
    try:
        # Initialize GitHub client
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        if verbose:
            print(f"Connected to repository: {repo.full_name}")
        
        # Check if release already exists
        try:
            existing_release = repo.get_release(tag_name)
            if verbose:
                print(f"Release with tag '{tag_name}' already exists")
            return existing_release
        except GithubException:
            # Release doesn't exist, continue with creation
            pass
        
        # Create the release
        if verbose:
            print("Creating release...")
        
        release = repo.create_git_release(
            tag=tag_name,
            name=release_name,
            message=release_notes,
            draft=False,
            prerelease=False
        )
        
        if verbose:
            print(f"✅ Release created successfully: {release.html_url}")
        
        # Upload the zip file as an asset
        if zip_file_path.exists():
            if verbose:
                print(f"Uploading asset: {zip_file_path.name}")
            
            asset = release.upload_asset(
                path=str(zip_file_path),
                label=f"Workshop data ({zip_file_path.name})",
                content_type="application/zip"
            )
            
            if verbose:
                print(f"✅ Asset uploaded successfully: {asset.browser_download_url}")
        else:
            if verbose:
                print(f"⚠️ Warning: Zip file '{zip_file_path}' not found, skipping asset upload")
        
        return release
        
    except GithubException as e:
        raise Exception(f"GitHub API error: {e}")
    except Exception as e:
        raise Exception(f"Error creating release: {e}")


app = typer.Typer(help="Utility script for working with workshop data archives")


@app.command()
def zip(
    source_dir: Optional[Path] = typer.Argument(
        None,
        help="Source directory to zip. Defaults to 'data' directory in script location."
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output zip file path. Defaults to '<source_dir>.zip'."
    ),
    verbose: bool = typer.Option(
        True,
        "--verbose/--quiet",
        "-v/-q",
        help="Enable verbose output showing files being added."
    )
):
    """
    Zip a directory and all its contents.
    
    If no source directory is provided, it will zip the 'data' directory
    in the same location as this script.
    """
    script_dir = Path(__file__).parent
    
    # Set default source directory if not provided
    if source_dir is None:
        source_dir = script_dir / "data"
    
    # Set default output filename if not provided
    if output is None:
        output = script_dir / f"{source_dir.name}.zip"
    
    # Enable/disable verbose output in zip_directory function
    try:
        zip_directory(source_dir, output, verbose)
        typer.echo(f"✅ Successfully created: {output}", color=True)
    except (FileNotFoundError, NotADirectoryError) as e:
        typer.echo(f"❌ Error: {e}", err=True, color=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True, color=True)
        raise typer.Exit(1)


@app.command()
def unzip(
    zip_file: Optional[Path] = typer.Argument(
        None,
        help="Zip file to extract. Defaults to 'data.zip' in script location."
    ),
    extract_to: Optional[Path] = typer.Option(
        None,
        "--extract-to",
        "-e",
        help="Directory to extract files to. Defaults to 'data' directory."
    ),
    verbose: bool = typer.Option(
        True,
        "--verbose/--quiet",
        "-v/-q",
        help="Enable verbose output showing files being extracted."
    )
):
    """
    Unzip an archive file.
    
    If no zip file is provided, it will extract 'data.zip' to the 'data' directory
    in the same location as this script.
    """
    script_dir = Path(__file__).parent
    
    # Set default zip file if not provided
    if zip_file is None:
        zip_file = script_dir / "data.zip"
    
    # Set default extraction directory if not provided
    if extract_to is None:
        # If zip_file is data.zip, extract to data directory
        # Otherwise, extract to a directory with the same name as the zip file (without extension)
        extract_to = script_dir
    
    try:
        unzip_archive(zip_file, extract_to, verbose)
        typer.echo(f"✅ Successfully extracted to: {extract_to}", color=True)
    except (FileNotFoundError, ValueError) as e:
        typer.echo(f"❌ Error: {e}", err=True, color=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True, color=True)
        raise typer.Exit(1)


@app.command()
def release(
    repo: str = typer.Option(
        ...,
        "--repo",
        "-r",
        help="GitHub repository in format 'owner/repo'"
    ),
    tag: str = typer.Option(
        ...,
        "--tag",
        "-t",
        help="Git tag name for the release (e.g., 'v1.0.0')"
    ),
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Release name. Defaults to tag name."
    ),
    notes: str = typer.Option(
        "Workshop data release",
        "--notes",
        "--message",
        "-m",
        help="Release notes/description"
    ),
    zip_file: Optional[Path] = typer.Option(
        None,
        "--zip-file",
        "-z",
        help="Zip file to upload as asset. Defaults to 'data.zip' in script location."
    ),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        help="GitHub personal access token. Can also be set via GITHUB_TOKEN environment variable."
    ),
    verbose: bool = typer.Option(
        True,
        "--verbose/--quiet",
        "-v/-q",
        help="Enable verbose output"
    )
):
    """
    Create a GitHub release and upload the data zip file as an asset.
    
    Requires a GitHub personal access token with 'repo' permissions.
    The token can be provided via --token option or GITHUB_TOKEN environment variable.
    
    Example:
        python data.py release --repo "myuser/myworkshop" --tag "v2025.08.07"
    """
    script_dir = Path(__file__).parent
    
    # Get GitHub token from parameter or environment variable
    github_token = token or os.getenv("GITHUB_TOKEN")
    if not github_token:
        typer.echo(
            "❌ GitHub token is required. Provide it via --token option or set GITHUB_TOKEN environment variable.",
            err=True,
            color=True
        )
        typer.echo(
            "💡 To create a token, go to: https://github.com/settings/tokens",
            color=True
        )
        raise typer.Exit(1)
    
    # Set default release name if not provided
    if name is None:
        name = tag
    
    # Set default zip file if not provided
    if zip_file is None:
        zip_file = script_dir / "data.zip"
    
    # Check if zip file exists, offer to create it if it doesn't
    if not zip_file.exists():
        should_create = typer.confirm(
            f"Zip file '{zip_file}' not found. Would you like to create it first?"
        )
        if should_create:
            try:
                data_dir = script_dir / "data"
                zip_directory(data_dir, zip_file, verbose)
                typer.echo(f"✅ Created zip file: {zip_file}", color=True)
            except Exception as e:
                typer.echo(f"❌ Error creating zip file: {e}", err=True, color=True)
                raise typer.Exit(1)
        else:
            typer.echo("⚠️ Proceeding without zip file asset", color=True)
    
    try:
        # TODO: Need a better way to create release notes
        release = create_github_release(
            repo_name=repo,
            tag_name=tag,
            release_name=name,
            release_notes=notes,
            zip_file_path=zip_file,
            github_token=github_token,
            verbose=verbose
        )
        
        typer.echo("🎉 Release created successfully!", color=True)
        typer.echo(f"🔗 Release URL: {release.html_url}", color=True)
        
    except Exception as e:
        typer.echo(f"❌ Error creating release: {e}", err=True, color=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
