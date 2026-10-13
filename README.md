# Garage Education website

Source of [www.garageeducation.org](https://www.garageeducation.org): free, open-source courses from Garage Education.

Built with [Hugo](https://gohugo.io) and the [HugoBlox](https://hugoblox.com) kit, imported as a Hugo module.

## Run it locally

Needs Hugo extended 0.167.0 or later, Go (for Hugo modules), and Node 22 or later.

```bash
npx --yes pnpm@10.14.0 install   # Tailwind and Pagefind
hugo server                     # http://localhost:1313
```

## Layout

| Path | What it holds |
| --- | --- |
| `content/docs/` | Courses, one folder per course |
| `content/blog/` | Blog posts |
| `content/_index.md` | Home page blocks |
| `data/authors/admin.yaml` | The Garage Education profile shown on the home page |
| `config/_default/` | Site, menu, and theme configuration |

## Deploy

Every push to `main` runs `.github/workflows/publish.yaml`. It builds the site, assumes an AWS role through GitHub OIDC, syncs `public/` to the S3 bucket, and invalidates both CloudFront distributions. Pull requests run the build only.

## License

Content is licensed under CC BY-NC-ND 4.0. See `LICENSE.md` for the code.
