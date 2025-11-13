import { OwnerModal } from '#components/modals';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('OwnerModal', () => {
  let component: OwnerModal;
  let fixture: ComponentFixture<OwnerModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OwnerModal],
    }).compileComponents();

    fixture = TestBed.createComponent(OwnerModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
