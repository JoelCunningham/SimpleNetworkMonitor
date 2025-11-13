import { EditOwnerForm } from '#components/forms';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('EditOwnerForm', () => {
  let component: EditOwnerForm;
  let fixture: ComponentFixture<EditOwnerForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditOwnerForm],
    }).compileComponents();

    fixture = TestBed.createComponent(EditOwnerForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
