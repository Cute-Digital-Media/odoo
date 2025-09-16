# Stage 1
FROM odoo:17.0 AS builder
USER root

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Cute-Digital-Media/odoo.git --depth 1 --branch 17.0-CDM /tmp/odoo_fork

# Stage 2
FROM odoo:17.0

# Copy changed files
COPY --from=builder /tmp/odoo_fork/addons/mass_mailing_themes/ /usr/lib/python3/dist-packages/odoo/addons/mass_mailing_themes/
COPY --from=builder /tmp/odoo_fork/custom_addons /usr/lib/python3/dist-packages/odoo/