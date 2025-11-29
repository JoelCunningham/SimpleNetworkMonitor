import { OwnerCard } from '#components/cards';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('OwnerCard', () => {
  let component: OwnerCard;
  let fixture: ComponentFixture<OwnerCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OwnerCard],
    }).compileComponents();

    fixture = TestBed.createComponent(OwnerCard);
    component = fixture.componentInstance;

    // Set required input
    component.owner = { id: 1, name: 'Test Owner', devices: [] };

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
