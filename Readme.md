# Arpon Nag — Personal Portfolio

Personal portfolio website for [arponnag.github.io](https://arponnag.github.io).

Built with the [Personal Bootstrap template](https://bootstrapmade.com/personal-free-resume-bootstrap-template/) and customized for Arpon Nag.

## Updating content

The easiest way to keep the site current:

1. Edit `data/profile.json` for education and experience
2. Replace `Arpon_NAG_CV-1-1-1.pdf` when your CV changes
3. Push to `master` — GitHub Actions rebuilds the site automatically

You can also run locally:

```bash
python scripts/build_profile.py
```

## LinkedIn auto-sync

LinkedIn does **not** offer a free public API for personal profiles, so the site cannot reliably pull your full LinkedIn profile on its own.

Practical options:

| Option | How it works |
|--------|----------------|
| **Recommended** | Update `data/profile.json` and your CV PDF, then push |
| **Optional paid sync** | Add a `PROXYCURL_API_KEY` GitHub secret, then the weekly GitHub Action can refresh your headline and summary from LinkedIn |
| **Manual** | Edit `index.html` directly for design or project changes |

To enable optional LinkedIn sync:

1. Create an API key at [Proxycurl](https://nubela.co/proxycurl/)
2. In GitHub repo settings, add secret `PROXYCURL_API_KEY`
3. Run the **Update portfolio** workflow manually or wait for the weekly schedule

## Sections

- About & Interests
- Education
- Experience
- Projects
- Skills
- Resume & Links
- Contact
