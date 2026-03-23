param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ArgsFromCaller
)

$scriptPath = Join-Path $PSScriptRoot "ib_account_query.py"

& conda run -n finance python $scriptPath @ArgsFromCaller
$exitCode = $LASTEXITCODE
exit $exitCode
