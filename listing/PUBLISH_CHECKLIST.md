# Publish checklist — DocVault Action

Repository: **https://github.com/nico-builds/docvault-docs-action**

## Steps

1. Accept [Marketplace Developer Agreement](https://docs.github.com/en/site-policy/github-terms/github-marketplace-developer-agreement)
2. **Releases → Draft v1.0.0**
3. Check **Publish this Action to the GitHub Marketplace**
4. Primary: **Documentation** or **Code quality** | Secondary: **Continuous integration**
5. Description from [`LISTING_DRAFT.md`](LISTING_DRAFT.md)
6. Tag `v1` for major pinning

Usage:

```yaml
uses: nico-builds/docvault-docs-action@v1
with:
  cursor-api-key: ${{ secrets.CURSOR_API_KEY }}
  mode: write
  ui: 'true'
```

See [`../docvault-app/docs/VERIFIED_PUBLISHER_ROADMAP.md`](../docvault-app/docs/VERIFIED_PUBLISHER_ROADMAP.md).
