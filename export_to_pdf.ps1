$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docxItem = Get-Item "D:\*\Bao_Cao\CHUONG_3_THIET_KE_VA_XAY_DUNG_HE_THONG_AIOT_BLACKBOX.docx"
    $docxPath = $docxItem.FullName
    $pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
    Write-Output "Opening DOCX: $docxPath"
    $doc = $word.Documents.Open($docxPath)
    Write-Output "Saving PDF: $pdfPath"
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    Write-Output "Word export to PDF finished successfully!"
    Write-Output "PDF file size: $((Get-Item $pdfPath).Length) bytes"
} finally {
    $word.Quit()
}
