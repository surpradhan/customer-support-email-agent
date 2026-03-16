# Technical Troubleshooting

## App Running Slowly
1. Clear your browser cache and cookies.
2. Ensure you're using a supported browser: Chrome (v90+), Firefox (v88+), Safari (v14+), Edge (v90+).
3. Disable browser extensions that may interfere with the application.
4. Check your internet connection speed — we recommend at least 5 Mbps for optimal performance.
5. If the problem persists, check our status page at status.example.com for any known incidents.

## File Upload Issues
- Maximum file size: 500MB per file (Starter), 2GB per file (Professional/Enterprise).
- Supported formats: PDF, DOCX, XLSX, PNG, JPG, GIF, MP4, CSV, ZIP.
- If an upload fails, check your internet connection and try again. For large files, use the desktop app which supports resumable uploads.
- Uploads may be blocked by your corporate firewall — contact your IT team to whitelist *.example.com.

## Email Notifications Not Arriving
1. Check your spam/junk folder.
2. Add no-reply@example.com to your email contacts or safe senders list.
3. Verify your email address is correct in Settings > Account > Profile.
4. If using a custom domain, ensure your IT team has whitelisted our sending IPs. Contact support for the current IP list.
5. Allow up to 15 minutes for notification emails to arrive during peak usage periods.

## API Integration Issues
- API documentation is available at docs.example.com/api.
- Rate limits: 100 requests/minute (Starter), 500/minute (Professional), 2000/minute (Enterprise).
- Authentication uses API keys generated in Settings > Developer > API Keys.
- All API responses use JSON format. For errors, check the `error.code` and `error.message` fields.
- If you receive 429 (Too Many Requests), implement exponential backoff in your client.

## Mobile App Issues
- Ensure you're running the latest version from the App Store or Google Play.
- Clear the app cache: Settings > App > Clear Cache.
- If the app crashes on launch, uninstall and reinstall it.
- Push notifications require notification permissions enabled in your device settings.
