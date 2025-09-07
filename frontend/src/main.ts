import { App } from '#/app';
import { appConfig } from '#/app.config';
import { bootstrapApplication } from '@angular/platform-browser';

bootstrapApplication(App, appConfig).catch((err) => console.error(err));
