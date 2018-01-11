import { ParserFrontendPage } from './app.po';

describe('parser-frontend App', () => {
  let page: ParserFrontendPage;

  beforeEach(() => {
    page = new ParserFrontendPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
