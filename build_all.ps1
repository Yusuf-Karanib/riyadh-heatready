$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$localPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$workspacePython = Join-Path $projectRoot "..\.venv\Scripts\python.exe"
if (Test-Path -LiteralPath $localPython) {
    $python = (Resolve-Path -LiteralPath $localPython).Path
}
elseif (Test-Path -LiteralPath $workspacePython) {
    $python = (Resolve-Path -LiteralPath $workspacePython).Path
}
else {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $pythonCommand) {
        throw "Python was not found. Install Python 3.12 and the packages in requirements.txt."
    }
    $python = $pythonCommand.Source
}

function Invoke-PythonStep {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Script
    )

    & $python $Script
    if ($LASTEXITCODE -ne 0) {
        throw "Build step failed: $Script (exit code $LASTEXITCODE)"
    }
}

function Invoke-Notebook {
    & $python -m nbconvert --to notebook --execute --inplace `
        "notebooks\02_main_analysis.ipynb" `
        "--ExecutePreprocessor.timeout=120"
    if ($LASTEXITCODE -ne 0) {
        throw "Notebook execution failed (exit code $LASTEXITCODE)"
    }
}

Push-Location $projectRoot
try {
    Invoke-PythonStep "src\verify_sources.py"
    Invoke-PythonStep "src\run_analysis.py"
    Invoke-PythonStep "src\analyze_tanager.py"
    Invoke-PythonStep "src\run_analysis.py"
    Invoke-PythonStep "src\build_submission_assets.py"
    Invoke-Notebook
    Invoke-PythonStep "src\check_outputs.py"
    Invoke-PythonStep "src\package_submission.py"
}
finally {
    Pop-Location
}
