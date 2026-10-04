param([string]$InputDirectory = 'data/scene-pilot-review/raw', [string]$OutputFile = 'data/scene-pilot-review/faces.json')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$faceDetectorType = [Windows.Media.FaceAnalysis.FaceDetector, Windows.Media.FaceAnalysis, ContentType=WindowsRuntime]
$storageFileType = [Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime]
$streamType = [Windows.Storage.Streams.IRandomAccessStreamWithContentType, Windows.Storage.Streams, ContentType=WindowsRuntime]
$decoderType = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType=WindowsRuntime]
$bitmapType = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType=WindowsRuntime]
$faceType = [Windows.Media.FaceAnalysis.DetectedFace, Windows.Media.FaceAnalysis, ContentType=WindowsRuntime]
$faceListType = [System.Collections.Generic.IList``1].MakeGenericType($faceType)
$asTaskMethod = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethodDefinition -and $_.GetGenericArguments().Count -eq 1 -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
function Await-Operation($operation, [Type]$resultType) {
    $task = $asTaskMethod.MakeGenericMethod($resultType).Invoke($null, @($operation))
    $task.GetAwaiter().GetResult()
}
$detector = Await-Operation ($faceDetectorType::CreateAsync()) $faceDetectorType
$results = @()
foreach ($file in Get-ChildItem -LiteralPath $InputDirectory -Filter '*.jpg') {
    $storage = Await-Operation ($storageFileType::GetFileFromPathAsync($file.FullName)) $storageFileType
    $stream = Await-Operation ($storage.OpenReadAsync()) $streamType
    $decoder = Await-Operation ($decoderType::CreateAsync($stream)) $decoderType
    $bitmap = Await-Operation ($decoder.GetSoftwareBitmapAsync()) $bitmapType
    $gray = $bitmapType::Convert($bitmap, [Windows.Graphics.Imaging.BitmapPixelFormat]::Gray8)
    $faces = @(Await-Operation ($detector.DetectFacesAsync($gray)) $faceListType)
    $boxes = @($faces | ForEach-Object { $box = $_.FaceBox; @([int]$box.X,[int]$box.Y,[int]($box.X+$box.Width),[int]($box.Y+$box.Height)) })
    $results += [pscustomobject]@{ image_id = $file.BaseName; face_boxes_flat = $boxes; count = $faces.Count }
    $gray.Dispose(); $bitmap.Dispose(); $stream.Dispose()
}
$results | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $OutputFile -Encoding UTF8
$results | Select-Object image_id,count | Format-Table
