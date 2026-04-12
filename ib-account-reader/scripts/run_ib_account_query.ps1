param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ArgsFromCaller
)

$scriptPath = Join-Path $PSScriptRoot "ib_account_query.py"
$uvProjectRoot = if ($env:UV_PROJECT_ROOT) { $env:UV_PROJECT_ROOT } else { "/home/znz/project/hedgefund" }
$condaEnvName = if ($env:CONDA_ENV_NAME) { $env:CONDA_ENV_NAME } else { "finance" }

if ($env:VIRTUAL_ENV) {
    $venvPythonUnix = Join-Path $env:VIRTUAL_ENV "bin/python"
    $venvPythonWindows = Join-Path $env:VIRTUAL_ENV "Scripts/python.exe"
    if (Test-Path $venvPythonUnix) {
        & $venvPythonUnix $scriptPath @ArgsFromCaller
        exit $LASTEXITCODE
    }
    if (Test-Path $venvPythonWindows) {
        & $venvPythonWindows $scriptPath @ArgsFromCaller
        exit $LASTEXITCODE
    }
}

$projectPythonUnix = Join-Path $uvProjectRoot ".venv/bin/python"
$projectPythonWindows = Join-Path $uvProjectRoot ".venv/Scripts/python.exe"
if (Test-Path $projectPythonUnix) {
    & $projectPythonUnix $scriptPath @ArgsFromCaller
    exit $LASTEXITCODE
}
if (Test-Path $projectPythonWindows) {
    & $projectPythonWindows $scriptPath @ArgsFromCaller
    exit $LASTEXITCODE
}

if (Get-Command uv -ErrorAction SilentlyContinue) {
    if (Test-Path $uvProjectRoot) {
        & uv run --project $uvProjectRoot python $scriptPath @ArgsFromCaller
        exit $LASTEXITCODE
    }
}

if (Get-Command conda -ErrorAction SilentlyContinue) {
    & conda run -n $condaEnvName python $scriptPath @ArgsFromCaller
    exit $LASTEXITCODE
}

Write-Error "No compatible Python runtime found. Tried `$env:VIRTUAL_ENV, $uvProjectRoot/.venv, uv project $uvProjectRoot, and conda env $condaEnvName."
exit 1
