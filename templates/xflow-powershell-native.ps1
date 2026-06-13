# XFlow PowerShell native command helpers.
#
# Purpose:
# - Avoid `2>&1 | Out-String` around native commands.
# - Judge native command success by process exit code.
# - Provide a composable pattern for Git, Claude, Bash, and other external tools.

Set-StrictMode -Version 3.0

function ConvertTo-XFlowNativeArgument {
    param([AllowNull()][string]$Argument)

    if ($null -eq $Argument) {
        return '""'
    }

    if ($Argument.Length -eq 0) {
        return '""'
    }

    if ($Argument -notmatch '[\s"]') {
        return $Argument
    }

    return '"' + ($Argument -replace '"', '\"') + '"'
}

function Join-XFlowNativeArguments {
    param([string[]]$ArgumentList)

    return (($ArgumentList | ForEach-Object { ConvertTo-XFlowNativeArgument $_ }) -join ' ')
}

function New-XFlowNativeResult {
    param(
        [string]$FilePath,
        [string[]]$ArgumentList,
        [string]$WorkingDirectory,
        [int]$ExitCode,
        [string]$Stdout,
        [string]$Stderr
    )

    return [pscustomobject]@{
        FilePath = $FilePath
        ArgumentList = $ArgumentList
        WorkingDirectory = $WorkingDirectory
        ExitCode = $ExitCode
        Stdout = $Stdout
        Stderr = $Stderr
        Succeeded = ($ExitCode -eq 0)
    }
}

function Assert-XFlowNativeSuccess {
    param(
        [Parameter(Mandatory = $true)]$Result,
        [string]$Message = "Native command failed"
    )

    if ($Result.ExitCode -ne 0) {
        $cmd = "$($Result.FilePath) $(Join-XFlowNativeArguments $Result.ArgumentList)"
        throw "$Message with exit code $($Result.ExitCode): $cmd`n$($Result.Stdout)`n$($Result.Stderr)"
    }

    return $Result
}

function Invoke-XFlowNative {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [string[]]$ArgumentList = @(),
        [string]$WorkingDirectory = (Get-Location).Path,
        [switch]$CaptureOutput,
        [switch]$AllowFailure
    )

    $stdoutFile = New-TemporaryFile
    $stderrFile = New-TemporaryFile

    try {
        $argumentString = Join-XFlowNativeArguments $ArgumentList
        $process = Start-Process `
            -FilePath $FilePath `
            -ArgumentList $argumentString `
            -WorkingDirectory $WorkingDirectory `
            -RedirectStandardOutput $stdoutFile `
            -RedirectStandardError $stderrFile `
            -Wait `
            -PassThru

        $stdout = Get-Content -LiteralPath $stdoutFile -Raw -ErrorAction SilentlyContinue
        $stderr = Get-Content -LiteralPath $stderrFile -Raw -ErrorAction SilentlyContinue
        $result = New-XFlowNativeResult `
            -FilePath $FilePath `
            -ArgumentList $ArgumentList `
            -WorkingDirectory $WorkingDirectory `
            -ExitCode $process.ExitCode `
            -Stdout $stdout `
            -Stderr $stderr

        if (-not $CaptureOutput) {
            if (-not [string]::IsNullOrEmpty($stdout)) {
                [Console]::Out.Write($stdout)
            }
            if (-not [string]::IsNullOrEmpty($stderr)) {
                [Console]::Error.Write($stderr)
            }
        }
    } finally {
        Remove-Item -LiteralPath $stdoutFile, $stderrFile -Force -ErrorAction SilentlyContinue
    }

    if (-not $AllowFailure) {
        Assert-XFlowNativeSuccess -Result $result | Out-Null
    }

    return $result
}

function Invoke-XFlowGit {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string[]]$GitArguments,
        [string]$WorkingDirectory = (Get-Location).Path,
        [switch]$CaptureOutput,
        [switch]$AllowFailure
    )

    return Invoke-XFlowNative `
        -FilePath "git" `
        -ArgumentList $GitArguments `
        -WorkingDirectory $WorkingDirectory `
        -CaptureOutput:$CaptureOutput `
        -AllowFailure:$AllowFailure
}
