import { BaseModal } from '#components/modals';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('BaseModal', () => {
  let component: BaseModal;
  let fixture: ComponentFixture<BaseModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BaseModal],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(BaseModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
