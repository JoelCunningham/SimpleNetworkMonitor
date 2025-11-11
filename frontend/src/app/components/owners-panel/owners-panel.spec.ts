import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { OwnersPanel } from '#components/partials/owners-panel';

describe('OwnersPanel', () => {
  let component: OwnersPanel;
  let fixture: ComponentFixture<OwnersPanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OwnersPanel],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(OwnersPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render "Add Owner" card full width when no owners', () => {
    component.owners = [];
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const addOwnerCard = compiled.querySelector('.add-owner-card');
    expect(addOwnerCard).toBeTruthy();
    expect(addOwnerCard?.classList.contains('full-width')).toBeTrue();
  });

  it('should render owner cards when owners exist', () => {
    component.owners = [
      { id: 1, name: 'Alice', devices: [] },
      { id: 2, name: 'Bob', devices: [] },
    ];
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const ownerCards = compiled.querySelectorAll('.owner-card');
    expect(ownerCards.length).toBe(2);
    expect(ownerCards[0].textContent).toContain('Alice');
    expect(ownerCards[1].textContent).toContain('Bob');
    const addOwnerCard = compiled.querySelector('.add-owner-card');
    expect(addOwnerCard?.classList.contains('full-width')).toBeFalse();
  });
});
