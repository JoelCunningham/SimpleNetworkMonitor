import { OwnerModal } from '#components/modals';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('OwnerModal', () => {
  let component: OwnerModal;
  let fixture: ComponentFixture<OwnerModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OwnerModal],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(OwnerModal);
    component = fixture.componentInstance;

    // Set required input
    component.owner = { id: 1, name: 'Test Owner', devices: [] };

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
