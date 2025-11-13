import { BaseModal } from '#components/modals';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('BaseModal', () => {
  let component: BaseModal;
  let fixture: ComponentFixture<BaseModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BaseModal],
    }).compileComponents();

    fixture = TestBed.createComponent(BaseModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
