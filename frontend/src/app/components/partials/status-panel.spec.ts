import { ComponentFixture, TestBed } from '@angular/core/testing';
import { StatusPanel } from '#components/partials/status-panel';

describe('StatusPanel', () => {
  let component: StatusPanel;
  let fixture: ComponentFixture<StatusPanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StatusPanel],
    }).compileComponents();

    fixture = TestBed.createComponent(StatusPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render last scan time', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('time')?.textContent).toContain('Never');
  });

  it('should render the live view button', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('button')?.textContent).toContain(
      'Live view'
    );
  });

  it('should toggle view mode and button class', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const button = compiled.querySelector('button');
    expect(button?.classList.contains('inactive')).toBe(false);

    button?.click();
    fixture.detectChanges();

    expect(component.isLiveView).toBe(false);
    expect(button?.classList.contains('inactive')).toBe(true);
  });
});
